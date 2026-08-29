#!/bin/sh
# Flash one named display with the firmware in the build tree, the documented way.
#
#   sudo sh hub-provision-one.sh 94:A9:90:CF:7D:04 [seconds]
#
# This wraps devices/trmnl_provision.py rather than replacing it. Doing it by hand on
# 29 August cost an evening: esptool write_flash at 0x0 writes the app and leaves the NVS
# at 0x9000 as it lands, so the display lost its Wi-Fi credentials and its token and went
# quiet. The provisioner writes both, in that order, and registers the MAC.
#
# Two things it adds, and both were the actual faults:
#
#  * **It picks the port by MAC.** Both displays are on the cable and the names swap
#    between ttyACM0 and ttyACM1 depending on which woke first, so a fixed --port is a coin
#    toss about which board gets written.
#  * **It resets the chip afterwards for real.** esptool says "Hard resetting via RTS pin"
#    and on a USB-Serial/JTAG there is no RTS, so the chip stays in the ROM bootloader:
#    permanently enumerated, never sleeping, never joining the network. It reads exactly
#    like a bricked board and is not one. `--before usb_reset run` is what leaves it.
set -eu

MAC=${1:?give the MAC, e.g. 94:A9:90:CF:7D:04}
WAIT=${2:-300}
TREE=/srv/lanternina/build/trmnl-firmware-v1.8.12-mdns
ENVNAME=TRMNL_7inch5_OG_DIY_Kit
MERGED="$TREE/.pio/build/$ENVNAME/merged_firmware.bin"
VENV=/srv/lanternina/tools/platformio-venv/bin

test -f "$MERGED" || { echo "no firmware at $MERGED"; exit 1; }

echo "waiting up to ${WAIT}s for $MAC"
PORT=""
i=0
while [ "$i" -lt "$WAIT" ]; do
    for CANDIDATE in /dev/ttyACM*; do
        [ -e "$CANDIDATE" ] || continue
        SERIAL=$(udevadm info -q property -n "$CANDIDATE" 2>/dev/null \
            | sed -n 's/^ID_SERIAL_SHORT=//p' | head -1)
        if [ "$SERIAL" = "$MAC" ]; then PORT="$CANDIDATE"; break; fi
    done
    [ -n "$PORT" ] && break
    i=$((i + 1))
    sleep 1
done
[ -n "$PORT" ] || { echo "$MAC did not appear in ${WAIT}s"; exit 2; }
echo "$MAC is on $PORT after ${i}s"

cd /opt/lanternina
PYTHONPATH=/opt/lanternina python3 devices/trmnl_provision.py \
    --port "$PORT" --firmware "$MERGED" --force --wait-seconds 60

echo "--- leaving the ROM bootloader for real"
"$VENV/python" "$VENV/esptool.py" --chip esp32s3 --port "$PORT" \
    --before usb_reset --after hard_reset run 2>&1 | tail -3
echo "done"
