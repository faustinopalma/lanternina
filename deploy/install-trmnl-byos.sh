#!/bin/sh
set -eu

base_url=${1:-http://lanternina.local:8080}
source_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)

install -d -m 0755 /opt/lanternina/devices /opt/lanternina/firmware
install -d -m 0700 /var/lib/lanternina/trmnl-backupsinstall -m 0644 "$source_dir/__init__.py" /opt/lanternina/devices/__init__.py
install -m 0644 "$source_dir/trmnl_byos.py" /opt/lanternina/devices/trmnl_byos.py
install -m 0644 "$source_dir/trmnl_provision.py" /opt/lanternina/devices/trmnl_provision.py
install -m 0644 "$source_dir/trmnl-ready.bmp" /opt/lanternina/trmnl-ready.bmp
install -m 0644 "$source_dir/lanternina-trmnl.service" /etc/systemd/system/lanternina-trmnl.service
install -m 0644 "$source_dir/lanternina-trmnl-provision@.service" /etc/systemd/system/lanternina-trmnl-provision@.service
install -m 0644 "$source_dir/99-lanternina-trmnl.rules" /etc/udev/rules.d/99-lanternina-trmnl.rules
sed 's/\r$//' "$source_dir/configure-trmnl-wifi.py" > /tmp/lanternina-configure-trmnl-wifi
install -m 0755 /tmp/lanternina-configure-trmnl-wifi /usr/local/sbin/lanternina-configure-trmnl-wifi

getent group lanternina >/dev/null || groupadd --system lanternina
install -d -o root -g lanternina -m 0750 /etc/lanternina
# Group-writable: the service runs as a normal user and this is the only path it writes.
install -d -o root -g lanternina -m 0770 /var/lib/lanternina/state
env_file=/etc/lanternina/trmnl-byos.env
registry_file=/etc/lanternina/trmnl-devices.json
if [ ! -f "$registry_file" ]; then
    printf '{"version":1,"devices":{}}\n' > "$registry_file"
fi
chown root:lanternina "$registry_file"
chmod 0640 "$registry_file"

umask 077
{
    printf 'TRMNL_BASE_URL=%s\n' "$base_url"
    printf 'TRMNL_SCREEN_FILE=/opt/lanternina/trmnl-ready.bmp\n'
    printf 'TRMNL_DEVICE_REGISTRY=%s\n' "$registry_file"
    printf 'TRMNL_REFRESH_RATE=600\n'
    printf 'TRMNL_STATUS_FILE=/var/lib/lanternina/state/trmnl-status.json\n'
    printf 'TRMNL_DEVICE_LOG_FILE=/var/lib/lanternina/state/device-logs.jsonl\n'
    printf 'TRMNL_USB_REFRESH_RATE=10\n'
    printf 'TRMNL_LOW_BATTERY_FILE=/opt/lanternina/trmnl-low-battery.bmp\n'
    printf 'TRMNL_CRITICAL_BATTERY_FILE=/opt/lanternina/trmnl-critical-battery.bmp\n'
    printf 'TRMNL_PORT=8080\n'
} > "$env_file"

systemctl daemon-reload
udevadm control --reload-rules
systemctl enable --now lanternina-trmnl.service