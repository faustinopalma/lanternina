"""Exercise the actual M5Stack button branches on a host compiler, without a camera."""

from __future__ import annotations

import argparse
import subprocess
import tempfile
from pathlib import Path


def between(source: str, start: str, end: str) -> str:
    assert source.count(start) == 1, start
    return source.split(start, 1)[1].split(end, 1)[0]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--compiler", default="c++")
    parser.add_argument("--source", type=Path,
                        default=Path(__file__).parent / "camera-m5stack/src/main.cpp")
    args = parser.parse_args()
    source = args.source.read_text(encoding="utf-8")
    boot = "bool wakingForStatus = " + between(
        source, "bool wakingForStatus = ", "\n}\n\nvoid loop()",
    )
    buttons = "static bool shutterArmed" + between(
        source, "static bool shutterArmed", "\n    if (millis() - lastInteraction",
    )
    sleep = between(source, "static void sleepWhenReleased() {", "\nvoid setup()")
    assert "esp_sleep_enable_ext0_wakeup(SHUTTER, 0)" in sleep
    assert "esp_sleep_enable_ext1_wakeup(1ULL << WAKE, ESP_EXT1_WAKEUP_ALL_LOW)" in sleep
    assert "gpio_hold_en(POWER_HOLD)" in sleep and "gpio_deep_sleep_hold_en()" in sleep
    assert "esp_sleep_enable_timer_wakeup" not in source
    harness = r'''
#include <cassert>
#include <cstdint>
#include <string>
#include <vector>
enum { LOW, HIGH, SHUTTER=4, WAKE=13 };
enum { ESP_SLEEP_WAKEUP_UNDEFINED, ESP_SLEEP_WAKEUP_EXT0, ESP_SLEEP_WAKEUP_EXT1 };
int levels[14];
int cause = ESP_SLEEP_WAKEUP_UNDEFINED;
uint32_t clockMs = 0;
bool usbTestMode = false;
const char *trigger = "boot";
std::vector<bool> captures;
uint32_t millis() { return clockMs; }
int digitalRead(int pin) { return levels[pin]; }
int esp_sleep_get_wakeup_cause() { return cause; }
void feedback(int) {}
void work(bool takePhoto) { captures.push_back(takePhoto); }
'''
    harness += "\nvoid bootAction() {\n" + boot + "\n}\n"
    harness += "\nvoid pollButtons() {\n" + buttons + "\n}\n"
    harness += r'''
void tick(uint32_t when, int shutter, int wake) {
    clockMs = when; levels[SHUTTER] = shutter; levels[WAKE] = wake; pollButtons();
}
int main() {
    for (int reason : {ESP_SLEEP_WAKEUP_UNDEFINED, ESP_SLEEP_WAKEUP_EXT0,
                       ESP_SLEEP_WAKEUP_EXT1}) {
        for (int shutter : {LOW, HIGH}) for (int wake : {LOW, HIGH}) {
            cause = reason; levels[SHUTTER] = shutter; levels[WAKE] = wake;
            captures.clear(); bootAction();
            assert(captures.size() == 1);
            assert(captures[0] == (reason == ESP_SLEEP_WAKEUP_EXT0 && wake == HIGH));
        }
    }
    captures.clear();
    tick(0, HIGH, HIGH); tick(31, HIGH, HIGH);
    tick(40, LOW, HIGH); tick(60, HIGH, HIGH); tick(95, HIGH, HIGH);
    assert(captures.empty());
    tick(100, LOW, HIGH); tick(131, LOW, HIGH);
    assert(captures == std::vector<bool>{true});
    tick(10000, LOW, HIGH);
    assert(captures.size() == 1);
    tick(10001, HIGH, HIGH); tick(10032, HIGH, HIGH);
    tick(10040, LOW, HIGH); tick(10071, LOW, HIGH);
    assert(captures == (std::vector<bool>{true, true}));
    tick(10100, HIGH, HIGH); tick(10131, HIGH, HIGH);
    tick(10200, LOW, LOW); tick(10231, LOW, LOW);
    assert(captures == (std::vector<bool>{true, true, false}));
    tick(20000, LOW, LOW); tick(20001, LOW, HIGH); tick(20032, LOW, HIGH);
    assert(captures.size() == 3);
    tick(20100, HIGH, HIGH); tick(20131, HIGH, HIGH);
    usbTestMode = true;
    tick(20200, LOW, HIGH); tick(20231, LOW, HIGH);
    assert(captures.size() == 3);
    usbTestMode = false;
    tick(20300, LOW, HIGH);
    assert(captures.size() == 3);
    tick(20400, HIGH, HIGH); tick(20431, HIGH, HIGH);
    tick(20500, HIGH, LOW); tick(20531, HIGH, LOW);
    assert(captures == (std::vector<bool>{true, true, false, false}));
}
'''
    with tempfile.TemporaryDirectory(prefix="m5stack-check-") as temporary:
        root = Path(temporary)
        source_path, executable = root / "controls.cpp", root / "controls"
        source_path.write_text(harness, encoding="utf-8")
        subprocess.run([args.compiler, "-std=c++11", "-Wall", "-Wextra", "-Werror",
                        str(source_path), "-o", str(executable)], check=True, timeout=60)
        subprocess.run([str(executable)], check=True, timeout=10)
        source_path.write_text(harness.replace("work(wakingForPhoto);", "work(true);"),
                               encoding="utf-8")
        subprocess.run([args.compiler, "-std=c++11", str(source_path), "-o", str(executable)],
                       check=True, timeout=60)
        negative = subprocess.run([str(executable)], capture_output=True, timeout=10)
        assert negative.returncode != 0, "negative control unexpectedly passed"
    print("PASS: 12 boot states, debounce, held/released buttons, wake priority, negative control")


if __name__ == "__main__":
    main()