#!/bin/bash
# Everything a machine needs before it can be the house, and nothing else.
#
# Until 24 August 2026 this did not exist. The hub had been built by hand over three weeks
# and the knowledge of what it needed lived in one filesystem: a new card meant guessing
# which apt packages had been installed and which of the seventeen units mattered. That is
# the porting problem, and it is not solved by a container image — cupsd, avahi-daemon and a
# scanner on the network are requirements of the machine either way. Measured on the hub the
# same day: the recursive dependency closure of what the code imports is 597 packages and
# 1378 MB installed, so an image would carry that and add an artefact to build for arm64.
#
# Run it with --check first. It changes nothing and says what is missing, which is also how
# it was verified: run against the working hub, it must find nothing.
#
#   sudo ./hub-install.sh --check
#   sudo ./hub-install.sh --install /tmp/lanternina.tar
#
# The tar is what `git archive` holds, so the file on the card is the committed file:
#
#   git archive HEAD devices shared orchestrator printing vision experiences -o lanternina.tar
#
# It does not write the environment files. Those carry the device key and the household id,
# which has no second copy and names the rows in Cosmos, so a script that invented them
# would produce a house that starts and then fails for a reason nobody can see. It reports
# which are missing and which names each one must set.
#
# `install-trmnl-byos.sh` predates this and does the display half of the same job — the two
# trmnl units, the udev rule, two of the directories. It is what installed the running hub
# and is left alone; on a new card this script covers all of it, and the two must not be run
# expecting different trees.

set -euo pipefail

TREE=/opt/lanternina
CONF=/etc/lanternina
STATE=/var/lib/lanternina/state
GROUP=lanternina
# The units run as this user with the group above. It owns nothing: the tree is read-only to
# it and the state directory is group-writable, which is what `ProtectSystem=strict` leaves.
RUNS_AS=fausto

# What the code imports, and the three commands it shells out to. Measured rather than
# recalled: `cv2`, `numpy` and `PIL` are imported by devices/read_page, devices/scan_sheet,
# devices/epaper, printing/render and vision/read_sheet; `lp`, `scanimage` and `avahi-browse`
# are run by print_sheet, scan_sheet and inventory. avahi-daemon is here because the display
# resolves `lanternina.local` by mDNS, which is answered by the machine and not by the code.
PACKAGES=(
    python3-opencv          # brings python3-numpy
    python3-pil
    cups                    # the queue the printer is reached through
    cups-client             # lp
    cups-ipp-utils
    sane-utils              # scanimage
    sane-airscan            # eSCL, so the scanner is reached over the network
    avahi-daemon
    avahi-utils             # avahi-browse
)

# `orchestrator/router.py` and `orchestrator/safety.py` are not importable here and are not
# meant to be: they need httpx and the Azure libraries, and this machine holds no cloud
# credentials — it asks the panel. Only `orchestrator/outgoing.py` is imported, by
# devices/run_experience.py, and it is stdlib and shared only.

# Enabled on the working hub on 24 August 2026. Everything else in deploy/ is `static`,
# reached by a timer or by a path unit, or is a template.
ENABLE=(
    lanternina-afternoon.timer
    lanternina-help.timer
    lanternina-picture.timer
    lanternina-reminders.timer
    lanternina-status.timer
    lanternina-backup.timer
    lanternina-scan.path
    lanternina-trmnl.service
)

# Each file and the names it must set. Values are not written here and not printed anywhere.
declare -A ENV_KEYS=(
    [panel.env]="LANTERNINA_PANEL_URL LANTERNINA_HOUSEHOLD LANTERNINA_DEVICE_KEY"
    [experience.env]="LANTERNINA_EXPERIENCE LANTERNINA_PRINTER"
    [scanner.env]="LANTERNINA_SHEETS_DIR LANTERNINA_SCANNER"
    [trmnl-byos.env]="TRMNL_BASE_URL TRMNL_SCREEN_FILE TRMNL_DEVICE_REGISTRY TRMNL_PORT LANTERNINA_JOBS_FILE"
)

missing=0

say_missing() {
    printf 'MISSING  %s\n' "$1"
    missing=$((missing + 1))
}

check() {
    for package in "${PACKAGES[@]}"; do
        dpkg-query -W -f='${Status}' "$package" 2>/dev/null | grep -q "install ok installed" ||
            say_missing "package $package"
    done
    getent group "$GROUP" >/dev/null || say_missing "group $GROUP"
    id -u "$RUNS_AS" >/dev/null 2>&1 || say_missing "user $RUNS_AS"
    for directory in "$TREE" "$CONF" "$STATE"; do
        [ -d "$directory" ] || say_missing "directory $directory"
    done
    # One module per package, so a tree that arrived half-extracted is not called present.
    for module in devices/afternoon.py shared/message.py orchestrator/outgoing.py \
        printing/render.py vision/read_sheet.py; do
        [ -f "$TREE/$module" ] || say_missing "$TREE/$module"
    done
    for file in "${!ENV_KEYS[@]}"; do
        if [ ! -f "$CONF/$file" ]; then
            say_missing "$CONF/$file, which must set: ${ENV_KEYS[$file]}"
            continue
        fi
        for key in ${ENV_KEYS[$file]}; do
            grep -qE "^$key=" "$CONF/$file" || say_missing "$key in $CONF/$file"
        done
    done
    for unit in "${ENABLE[@]}"; do
        [ -f "/etc/systemd/system/$unit" ] || { say_missing "unit $unit"; continue; }
        [ "$(systemctl is-enabled "$unit" 2>/dev/null)" = enabled ] ||
            say_missing "$unit is not enabled"
    done
    [ -f /etc/udev/rules.d/99-lanternina-trmnl.rules ] ||
        say_missing "/etc/udev/rules.d/99-lanternina-trmnl.rules, so no display can be enrolled"
    if [ "$missing" -eq 0 ]; then
        echo "this machine has everything the house needs"
    fi
    return $((missing > 0))
}

install_tree() {
    local tar="$1"
    [ -f "$tar" ] || { echo "no such archive: $tar" >&2; exit 1; }
    apt-get update
    apt-get install -y --no-install-recommends "${PACKAGES[@]}"
    groupadd -f "$GROUP"
    install -d -o root -g root -m 755 "$TREE"
    install -d -o root -g "$GROUP" -m 750 "$CONF"
    install -d -o root -g "$GROUP" -m 770 "$STATE"
    # --no-same-owner, then the ownership set explicitly: a file whose group changes under a
    # service that reads it by group stops being readable, and the symptom is a dead display
    # rather than a permission error anybody would look for.
    tar -x --no-same-owner -C "$TREE" -f "$tar"
    chown -R root:root "$TREE"
    find "$TREE" -type d -exec chmod 755 {} +
    find "$TREE" -type f -exec chmod 644 {} +
    install -o root -g root -m 644 "$(dirname "$0")"/lanternina-*.service \
        "$(dirname "$0")"/lanternina-*.timer "$(dirname "$0")"/lanternina-*.path \
        /etc/systemd/system/
    install -o root -g root -m 755 "$(dirname "$0")/lanternina-backup" /usr/local/sbin/
    # Without this a card can serve the displays it already knows and can never enrol a new
    # one: the provisioner reaches a board over USB, and the port only exists while it is awake.
    install -o root -g root -m 644 "$(dirname "$0")/99-lanternina-trmnl.rules" \
        /etc/udev/rules.d/
    udevadm control --reload-rules
    systemctl daemon-reload
    # The environment files come last and are not created: the timers would otherwise start
    # asking a panel they have no address for.
    systemctl enable "${ENABLE[@]}"
    echo "installed. Now write $CONF, then --check."
}

case "${1:---check}" in
--check) check ;;
--install) install_tree "${2:?an archive to extract}" ;;
*) echo "usage: $0 [--check | --install <tar>]" >&2; exit 2 ;;
esac
