from __future__ import annotations

import argparse
import subprocess
import tempfile
from pathlib import Path


def between(source: str, start: str, end: str) -> str:
    assert source.count(start) == 1, start
    return source.split(start, 1)[1].split(end, 1)[0]


def main() -> None:
    parser = argparse.ArgumentParser(description="Run host checks on patched TRMNL source")
    parser.add_argument("tree", type=Path)
    args = parser.parse_args()
    logic = (args.tree / "src/bl.cpp").read_text(encoding="utf-8")
    display = (args.tree / "src/display.cpp").read_text(encoding="utf-8")
    retry = "static void wifiErrorDeepSleep()\n{" + between(
        logic, "static void wifiErrorDeepSleep()\n{", "\nDeviceStatusStamp"
    )
    pins = "static const int lanterninaPins[] = " + between(
        logic, "static const int lanterninaPins[] = ", ";"
    ) + ";"
    selection = between(
        logic, "#ifdef LANTERNINA_DISPLAY\n  if (gpio_wakeup)",
        "#else\n  if (gpio_wakeup)",
    )
    selection = "if (gpio_wakeup)" + selection
    wake = "uint64_t released = 0;" + between(
        logic, "#if defined(LANTERNINA_DISPLAY)\n  uint64_t released = 0;",
        "#elif CONFIG_IDF_TARGET_ESP32",
    )
    source = "if (lanterninaButton == 1)" + between(
        logic, "  if (lanterninaButton == 1)", "#endif"
    )
    renderer = "void display_show_lanternina(" + between(
        display, "void display_show_lanternina(", "\nstatic void display_lanternina_message"
    )
    assert "resetSettings" not in selection and "resetDeviceCredentials" not in selection
    assert "read_button_presses" not in selection
    assert "esp_sleep_enable_timer_wakeup" in between(
        logic, "void goToSleep(void)\n{", "static void goToSleepButtonOnly(void)\n{"
    )
    harness = r'''
#include <cassert>
#include <cstdint>
#include <string>
#include <vector>
#define Log_info(...) ((void)0)
enum { PREFERENCES_CONNECT_WIFI_RETRY_COUNT, PREFERENCES_SLEEP_TIME_KEY };
enum WIFI_CONNECT_RETRY_TIME { WIFI_FIRST_RETRY=60, WIFI_SECOND_RETRY=180,
                             WIFI_THIRD_RETRY=300 };
struct Preferences {
    int counter=1;
    unsigned int seconds=0;
    bool exists=true;
    bool isKey(int) { return exists; }
    int getInt(int) { return counter; }
    void putInt(int, int value) { counter=value; exists=true; }
    void putUInt(int, unsigned int value) { seconds=value; }
} preferences;
int timedSleeps=0, buttonOnlySleeps=0, displaySleeps=0;
void display_sleep() { ++displaySleeps; }
void goToSleep() { ++timedSleeps; }
void goToSleepButtonOnly() { ++buttonOnlySleeps; }
enum { LOW, HIGH, ESP_SLEEP_WAKEUP_EXT0, ESP_SLEEP_WAKEUP_EXT1, ESP_EXT1_WAKEUP_ANY_LOW };
int levels[6]={HIGH,HIGH,HIGH,HIGH,HIGH,HIGH};
int digitalRead(int pin) { return levels[pin]; }
uint64_t wakeStatus=0, wakeMask=0;
int disabled=0, wakeup_reason=ESP_SLEEP_WAKEUP_EXT1, lanterninaButton=0;
bool gpio_wakeup=true;
uint64_t esp_sleep_get_ext1_wakeup_status() { return wakeStatus; }
void esp_sleep_disable_wakeup_source(int) { ++disabled; }
void esp_sleep_enable_ext1_wakeup(uint64_t mask, int mode) {
    assert(mode==ESP_EXT1_WAKEUP_ANY_LOW); wakeMask=mask;
}
void wait_for_serial() {}
struct { std::string updateSource; } inputs;
enum { BBEP_SUCCESS=0, BBEP_ERROR_NO_MEMORY=3, BBEP_WHITE, BBEP_BLACK,
       REFRESH_FULL, PLANE_0, nicoclean_8 };
struct BB_RECT { int w=0; };
struct Display {
    int allocation=BBEP_SUCCESS, frees=0;
    std::vector<std::string> lines;
    int allocBuffer(bool) { return allocation; }
    void fillScreen(int) {}
    void setFont(int) {}
    void setTextColor(int,int) {}
    void getStringBox(const char*,BB_RECT*) {}
    int width() { return 800; }
    void setCursor(int,int) {}
    void print(const char* text) { lines.push_back(text); }
    void freeBuffer() { ++frees; }
} bbep;
int refreshes=0;
void display_update_epaper(int,bool,bool,int) { ++refreshes; }
'''
    harness += pins + retry + renderer
    harness += "\nvoid selectButton() {" + selection + "}\n"
    harness += "void armWake() {" + wake + "}\n"
    harness += "void setSource() {" + source + "}\n"
    harness += r'''
int main() {
    preferences.exists=false;
    for (int attempt=0; attempt<1000; ++attempt) {
        wifiErrorDeepSleep();
        assert(preferences.seconds==(attempt==0 ? 60U : attempt==1 ? 180U : 300U));
        assert(preferences.counter==(attempt==0 ? 2 : 3));
    }
    for (int stale : {-1,0,4,255,256,2147483647}) {
        preferences.counter=stale;
        wifiErrorDeepSleep();
        assert(preferences.seconds==300 && preferences.counter==3);
    }
    assert(timedSleeps==1006 && displaySleeps==1006 && buttonOnlySleeps==0);
    for (int held=0; held<8; ++held) {
        uint64_t expected=0;
        for (int index=0; index<3; ++index) {
            levels[lanterninaPins[index]]=(held & (1<<index)) ? LOW : HIGH;
            if (levels[lanterninaPins[index]]==HIGH) expected|=1ULL<<lanterninaPins[index];
        }
        wakeMask=0; disabled=0; armWake();
        assert(wakeMask==expected && disabled==2);
    }
    for (int pin : lanterninaPins) levels[pin]=HIGH;
    for (int index=0; index<3; ++index) {
        wakeStatus=1ULL<<lanterninaPins[index];
        lanterninaButton=0; selectButton();
        assert(lanterninaButton==index+1);
        setSource();
        const char* expected[]={"lanternina-refresh","lanternina-status","EXT0"};
        assert(inputs.updateSource==expected[index]);
        levels[lanterninaPins[index]]=LOW;
        for (int repeat=0; repeat<100; ++repeat) {
            lanterninaButton=0; selectButton(); assert(lanterninaButton==index+1);
        }
        levels[lanterninaPins[index]]=HIGH;
    }
    wakeStatus=0; wakeup_reason=ESP_SLEEP_WAKEUP_EXT0;
    lanterninaButton=0; selectButton(); assert(lanterninaButton==3);
    gpio_wakeup=false; lanterninaButton=0;
    selectButton(); assert(lanterninaButton==0);
    display_show_lanternina("connection","battery","identity");
    assert(refreshes==1 && bbep.frees==1 && bbep.lines.size()==4);
    assert(bbep.lines[0]=="LANTERNINA");
    bbep.allocation=BBEP_ERROR_NO_MEMORY;
    display_show_lanternina("connection","battery","identity");
    assert(refreshes==1 && bbep.frees==1);
}
'''
    with tempfile.TemporaryDirectory(prefix="lanternina-firmware-check-") as folder:
        directory = Path(folder)
        for negative in (False, True):
            candidate = harness
            if negative:
                broken = retry.replace("goToSleep();", "goToSleepButtonOnly();")
                assert broken != retry
                candidate = candidate.replace(retry, broken)
            source_file = directory / "check.cpp"
            executable = directory / "check"
            source_file.write_text(candidate, encoding="utf-8")
            subprocess.run(
                ["g++", "-std=c++17", "-Wall", str(source_file), "-o", str(executable)],
                check=True,
            )
            result = subprocess.run([str(executable)], capture_output=True)
            assert (result.returncode != 0) == negative, result.stderr.decode()
    print("PASS: 1006 retry states, 8 held-key masks, 3 commands, renderer, negative control")


if __name__ == "__main__":
    main()