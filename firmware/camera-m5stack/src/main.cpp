#include <Arduino.h>
#include <ArduinoJson.h>
#include <HTTPClient.h>
#include <LittleFS.h>
#include <WiFi.h>
#include <WiFiClientSecure.h>
#include <driver/gpio.h>
#include <driver/rtc_io.h>
#include <esp_camera.h>
#include <esp_sleep.h>
#include <esp_system.h>
#include <time.h>
#include "camera_secrets.h"

static constexpr gpio_num_t SHUTTER = GPIO_NUM_4;
static constexpr gpio_num_t WAKE = GPIO_NUM_13;
static constexpr gpio_num_t POWER_HOLD = GPIO_NUM_33;
static constexpr gpio_num_t SENSOR_RESET = GPIO_NUM_15;
static constexpr int LED = 2;
static constexpr uint32_t AWAKE_MS = 120000;
static constexpr uint32_t NETWORK_MS = 20000;
static constexpr size_t MAX_JPEG = 750000;
static constexpr int QUEUE_LIMIT = 3;
static constexpr int WARMUP_FRAMES = 2;
static const char *FIRMWARE = "m5stack-2026-10-02-external-controls";
static bool storageReady = false;
static bool identityReady = false;
static bool usbTestMode = false;
static bool captureRequested = false;
static uint32_t lastInteraction = 0;
static uint32_t bootTag = 0;
static const char *captureResult = "not_requested";
static const char *trigger = "boot";
static const char *networkResult = "not_attempted";
static String captureId;
static String uploadId;
static uint32_t captureMs = 0, sensorInitMs = 0, frameReadyMs = 0, storageMs = 0;
static uint32_t uploadMs = 0, workMs = 0;
static size_t jpegBytes = 0, frameWidth = 0, frameHeight = 0;
static int uploadHttp = 0;
static bool uploadAccepted = false;
static bool previousSleepConfirmed = false;
static double sleepSeconds = -1;
RTC_DATA_ATTR static uint32_t sleepMarker = 0;
RTC_DATA_ATTR static uint32_t sleepingBoot = 0;
RTC_DATA_ATTR static time_t sleepingAt = 0;
RTC_DATA_ATTR static uint32_t wakeCount = 0;

static const char *wakeCause() {
    switch (esp_sleep_get_wakeup_cause()) {
        case ESP_SLEEP_WAKEUP_EXT0: return "button";
        case ESP_SLEEP_WAKEUP_EXT1: return "wake_button";
        case ESP_SLEEP_WAKEUP_TIMER: return "timer";
        case ESP_SLEEP_WAKEUP_UNDEFINED: return "not_deep_sleep";
        default: return "other";
    }
}

static const char *resetReason() {
    switch (esp_reset_reason()) {
        case ESP_RST_DEEPSLEEP: return "deep_sleep";
        case ESP_RST_POWERON: return "power_on";
        case ESP_RST_BROWNOUT: return "brownout";
        case ESP_RST_PANIC: return "panic";
        case ESP_RST_TASK_WDT: return "task_watchdog";
        case ESP_RST_INT_WDT: return "interrupt_watchdog";
        case ESP_RST_SW: return "software";
        case ESP_RST_EXT: return "external_reset";
        default: return "other";
    }
}

static String identifier() {
    char value[33];
    snprintf(value, sizeof(value), "%08lx%08lx%08lx%08lx",
             (unsigned long)esp_random(), (unsigned long)esp_random(),
             (unsigned long)esp_random(), (unsigned long)esp_random());
    return String(value);
}

static String queuePath(const String &id) {
    return "/" + id.substring(0, 24);
}

static int queued() {
    int count = 0;
    File root = LittleFS.open("/");
    for (File entry = root.openNextFile(); entry; entry = root.openNextFile()) {
        if (String(entry.name()).endsWith(".json")) ++count;
    }
    return count;
}

static void feedback(int flashes) {
    for (int flash = 0; flash < flashes; ++flash) {
        digitalWrite(LED, HIGH);
        delay(150);
        digitalWrite(LED, LOW);
        delay(150);
    }
}

static bool captureFailed(const char *reason) {
    digitalWrite(LED, LOW);
    digitalWrite(SENSOR_RESET, LOW);
    captureResult = reason;
    Serial.printf("capture_failed=%s\n", reason);
    return false;
}

static bool capture() {
    if (!storageReady) return captureFailed("filesystem_unavailable");
    if (queued() >= QUEUE_LIMIT) return captureFailed("queue_full");
    if (LittleFS.totalBytes() - LittleFS.usedBytes() < MAX_JPEG + 8192) {
        return captureFailed("storage_full");
    }
    if (!psramFound()) return captureFailed("psram_unavailable");
    uint32_t capturedMillis = millis();
    time_t capturedEpoch = time(nullptr);
    digitalWrite(LED, HIGH);
    camera_config_t config = {};
    config.ledc_channel = LEDC_CHANNEL_0;
    config.ledc_timer = LEDC_TIMER_0;
    config.pin_d0 = 32; config.pin_d1 = 35; config.pin_d2 = 34; config.pin_d3 = 5;
    config.pin_d4 = 39; config.pin_d5 = 18; config.pin_d6 = 36; config.pin_d7 = 19;
    config.pin_xclk = 27; config.pin_pclk = 21;
    config.pin_vsync = 22; config.pin_href = 26;
    config.pin_sccb_sda = 25; config.pin_sccb_scl = 23;
    config.pin_pwdn = -1; config.pin_reset = SENSOR_RESET;
    config.xclk_freq_hz = 20000000;
    config.pixel_format = PIXFORMAT_JPEG;
    config.frame_size = FRAMESIZE_UXGA;
    config.jpeg_quality = 12;
    config.fb_count = 1;
    config.fb_location = CAMERA_FB_IN_PSRAM;
    config.grab_mode = CAMERA_GRAB_WHEN_EMPTY;
    esp_err_t initialized = esp_camera_init(&config);
    sensorInitMs = millis() - capturedMillis;
    if (initialized != ESP_OK) {
        Serial.printf("camera_init_error=0x%x\n", initialized);
        return captureFailed("sensor_initialization");
    }
    sensor_t *sensor = esp_camera_sensor_get();
    if (!sensor || sensor->id.PID != OV3660_PID ||
        sensor->set_exposure_ctrl(sensor, 1) != 0 ||
        sensor->set_gain_ctrl(sensor, 1) != 0 || sensor->set_whitebal(sensor, 1) != 0 ||
        sensor->set_vflip(sensor, 1) != 0 || sensor->set_hmirror(sensor, 0) != 0) {
        esp_camera_deinit();
        return captureFailed("sensor_or_controls");
    }
    Serial.printf("sensor=%04x psram=%u warmup_frames=%d\n",
                  sensor->id.PID, ESP.getPsramSize(), WARMUP_FRAMES);
    for (int frame = 0; frame < WARMUP_FRAMES; ++frame) {
        camera_fb_t *warmup = esp_camera_fb_get();
        if (!warmup) {
            esp_camera_deinit();
            return captureFailed("warmup_frame");
        }
        esp_camera_fb_return(warmup);
        delay(80);
    }
    camera_fb_t *image = esp_camera_fb_get();
    frameReadyMs = millis() - capturedMillis;
    digitalWrite(LED, LOW);
    uint32_t storageBegan = millis();
    bool saved = false;
    if (image) {
        jpegBytes = image->len;
        frameWidth = image->width;
        frameHeight = image->height;
        Serial.printf("frame width=%u height=%u bytes=%u\n",
                      image->width, image->height, image->len);
    }
    if (image && image->format == PIXFORMAT_JPEG && image->len > 0 && image->len <= MAX_JPEG) {
        String id, path;
        do {
            id = identifier();
            path = queuePath(id);
        } while (LittleFS.exists(path + ".json") || LittleFS.exists(path + ".jpg") ||
                 LittleFS.exists(path + ".part") || LittleFS.exists(path + ".meta"));
        captureId = id;
        File temporary = LittleFS.open(path + ".part", "w");
        saved = temporary && temporary.write(image->buf, image->len) == image->len;
        temporary.flush(); temporary.close();
        File verify = LittleFS.open(path + ".part", "r");
        saved = saved && verify && verify.size() == image->len;
        uint8_t chunk[1024];
        for (size_t offset = 0; saved && offset < image->len;) {
            size_t expected = min(sizeof(chunk), image->len - offset);
            size_t read = verify.read(chunk, expected);
            saved = read == expected && memcmp(chunk, image->buf + offset, read) == 0;
            offset += read;
        }
        verify.close();
        saved = saved && LittleFS.rename(path + ".part", path + ".jpg");
        if (saved) {
            StaticJsonDocument<256> record;
            record["id"] = id;
            record["boot"] = bootTag;
            record["millis"] = capturedMillis;
            record["epoch"] = capturedEpoch > 1700000000 ? capturedEpoch : 0;
            record["diagnostic"] = strcmp(trigger, "usb_command") == 0;
            File metadata = LittleFS.open(path + ".meta", "w");
            saved = metadata && serializeJson(record, metadata) > 0;
            metadata.flush(); metadata.close();
            saved = saved && LittleFS.rename(path + ".meta", path + ".json");
        }
        Serial.printf("capture=%s bytes=%u saved=%d\n", id.c_str(), image->len, saved);
        if (!saved) {
            LittleFS.remove(path + ".part");
            LittleFS.remove(path + ".meta");
            LittleFS.remove(path + ".jpg");
        }
    }
    storageMs = millis() - storageBegan;
    if (image) esp_camera_fb_return(image);
    esp_camera_deinit();
    digitalWrite(SENSOR_RESET, LOW);
    if (!saved) return captureFailed("frame_or_storage");
    captureResult = "saved";
    return true;
}

static bool connectForReport() {
    WiFi.mode(WIFI_STA);
    WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
    uint32_t began = millis();
    while (WiFi.status() != WL_CONNECTED && millis() - began < NETWORK_MS) delay(50);
    if (WiFi.status() != WL_CONNECTED) { networkResult = "wifi_timeout"; return false; }
    configTime(0, 0, "pool.ntp.org");
    began = millis();
    while (time(nullptr) < 1700000000 && millis() - began < 10000) delay(50);
    if (time(nullptr) < 1700000000) { networkResult = "clock_unset"; return false; }
    networkResult = "connected";
    return true;
}

static void reportStatus(const char *phase) {
    if (WiFi.status() != WL_CONNECTED || time(nullptr) < 1700000000) return;
    WiFiClientSecure tls;
    tls.setCACert(HUB_CA);
    tls.setHandshakeTimeout(10);
    HTTPClient http;
    http.setConnectTimeout(5000);
    http.setTimeout(10000);
    if (!http.begin(tls, String(HUB_URL) + "/status")) return;
    StaticJsonDocument<2048> status;
    status["board"] = "m5stack-timer-camera";
    status["firmware"] = FIRMWARE;
    status["usb"] = nullptr;
    status["voltage"] = nullptr;
    status["rssi"] = WiFi.RSSI();
    status["captureResult"] = captureResult;
    status["queued"] = storageReady ? queued() : -1;
    JsonObject diagnostics = status.createNestedObject("diagnostics");
    diagnostics["captureRequested"] = captureRequested;
    diagnostics["phase"] = phase;
    diagnostics["bootId"] = String(bootTag, HEX);
    diagnostics["previousBootId"] = String(previousSleepConfirmed ? sleepingBoot : 0, HEX);
    diagnostics["wakeCause"] = wakeCause();
    diagnostics["resetReason"] = resetReason();
    diagnostics["resetCode"] = (int)esp_reset_reason();
    diagnostics["previousSleepConfirmed"] = previousSleepConfirmed;
    diagnostics["previousSleepAt"] = (long long)(previousSleepConfirmed ? sleepingAt : 0);
    diagnostics["sleepSeconds"] = sleepSeconds;
    diagnostics["wakeCount"] = wakeCount;
    diagnostics["trigger"] = trigger;
    diagnostics["captureResult"] = captureResult;
    diagnostics["captureId"] = captureId;
    diagnostics["uploadId"] = uploadId;
    diagnostics["captureMs"] = captureMs;
    diagnostics["sensorInitMs"] = sensorInitMs;
    diagnostics["frameReadyMs"] = frameReadyMs;
    diagnostics["storageMs"] = storageMs;
    diagnostics["uploadMs"] = uploadMs;
    diagnostics["workMs"] = workMs;
    diagnostics["jpegBytes"] = jpegBytes;
    diagnostics["width"] = frameWidth;
    diagnostics["height"] = frameHeight;
    diagnostics["uploadHttp"] = uploadHttp;
    diagnostics["uploadAccepted"] = uploadAccepted;
    diagnostics["networkResult"] = networkResult;
    diagnostics["queued"] = storageReady ? queued() : -1;
    diagnostics["freeHeap"] = ESP.getFreeHeap();
    diagnostics["freePsram"] = ESP.getFreePsram();
    diagnostics["filesystemUsed"] = storageReady ? LittleFS.usedBytes() : 0;
    diagnostics["filesystemTotal"] = storageReady ? LittleFS.totalBytes() : 0;
    diagnostics["uptimeMs"] = millis();
    diagnostics["buttonPressed"] = digitalRead(SHUTTER) == LOW;
    diagnostics["clockSet"] = time(nullptr) >= 1700000000;
    http.addHeader("Authorization", String("Bearer ") + CAMERA_TOKEN);
    http.addHeader("X-Camera-Id", CAMERA_ID);
    http.addHeader("Content-Type", "application/json");
    String body;
    serializeJson(status, body);
    Serial.printf("diagnostics=%s\n", body.c_str());
    Serial.printf("status_http=%d phase=%s\n", http.POST(body), phase);
    http.end();
}

static bool deliver() {
    File root = LittleFS.open("/");
    for (File entry = root.openNextFile(); entry; entry = root.openNextFile()) {
        if (!String(entry.name()).endsWith(".json")) continue;
        StaticJsonDocument<256> record;
        DeserializationError parseError = deserializeJson(record, entry);
        entry.close();
        if (parseError) return false;
        String id = record["id"].as<String>();
        String path = queuePath(id);
        File image = LittleFS.open(path + ".jpg", "r");
        if (!image || image.size() == 0) return false;
        WiFiClientSecure tls;
        tls.setCACert(HUB_CA);
        tls.setHandshakeTimeout(10);
        HTTPClient http;
        http.setConnectTimeout(5000);
        http.setTimeout(15000);
        if (!http.begin(tls, String(HUB_URL) + "/photos/" + id)) return false;
        http.addHeader("Authorization", String("Bearer ") + CAMERA_TOKEN);
        http.addHeader("Content-Type", "image/jpeg");
        http.addHeader("X-Camera-Id", CAMERA_ID);
        if (record["diagnostic"] == true) http.addHeader("X-Capture-Purpose", "diagnostic");
        if (record["epoch"].as<long long>() > 1700000000) {
            http.addHeader("X-Captured-At", String(record["epoch"].as<long long>()));
        } else if (record["boot"].as<uint32_t>() == bootTag) {
            http.addHeader("X-Capture-Age", String((millis() - record["millis"].as<uint32_t>()) / 1000));
        }
        uint32_t uploadBegan = millis();
        int status = http.sendRequest("PUT", &image, image.size());
        image.close();
        StaticJsonDocument<256> receipt;
        bool accepted = status == 201 || status == 200;
        accepted = accepted && !deserializeJson(receipt, http.getString());
        accepted = accepted && receipt["id"].as<String>() == id && receipt["stored"] == true;
        uploadMs = millis() - uploadBegan;
        uploadHttp = status;
        uploadAccepted = accepted;
        uploadId = id;
        http.end();
        Serial.printf("upload=%s status=%d accepted=%d\n", id.c_str(), status, accepted);
        if (!accepted || !LittleFS.remove(path + ".json")) return false;
        LittleFS.remove(path + ".jpg");
        feedback(2);
    }
    return true;
}

static void work(bool takePhoto, bool sleepOnly = false) {
    if (!identityReady) return;
    uint32_t began = millis();
    captureRequested = takePhoto;
    if (takePhoto) {
        captureId = ""; uploadId = "";
        jpegBytes = 0; frameWidth = 0; frameHeight = 0;
        uploadHttp = 0; uploadMs = 0; uploadAccepted = false;
        sensorInitMs = 0; frameReadyMs = 0; storageMs = 0;
        captureResult = "started";
        bool captured = capture();
        captureMs = millis() - began;
        if (!captured) feedback(3);
    }
    if (connectForReport()) {
        if (!sleepOnly) {
            reportStatus("before_upload");
            if (storageReady) deliver();
        }
        workMs = millis() - began;
        reportStatus(sleepOnly ? "sleep_planned" : "operation_complete");
    }
    WiFi.disconnect(true);
    WiFi.mode(WIFI_OFF);
    if (!sleepOnly) lastInteraction = millis();
    Serial.printf("busy=0 filesystem=%d queued=%d\n",
                  storageReady, storageReady ? queued() : -1);
}

static void status() {
    Serial.printf("board=m5stack-timer-camera firmware=%s wake_gpio=%d led_gpio=%d\n",
                  FIRMWARE, (int)WAKE, LED);
    Serial.printf("status usb=unknown busy=0 psram=%u filesystem=%d queued=%d "
                  "last_capture=%s identity=%s button_gpio=%d usb_test=%d\n",
                  ESP.getPsramSize(), storageReady, storageReady ? queued() : -1,
                  captureResult, CAMERA_ID, (int)SHUTTER, usbTestMode);
}

static void sleepWhenReleased() {
    if (digitalRead(SHUTTER) == LOW || digitalRead(WAKE) == LOW) return;
    work(false, true);
    if (digitalRead(SHUTTER) == LOW || digitalRead(WAKE) == LOW) return;
    rtc_gpio_pullup_en(SHUTTER);
    rtc_gpio_pulldown_dis(SHUTTER);
    rtc_gpio_pullup_en(WAKE);
    rtc_gpio_pulldown_dis(WAKE);
    esp_sleep_pd_config(ESP_PD_DOMAIN_RTC_PERIPH, ESP_PD_OPTION_ON);
    esp_err_t shutterWake = esp_sleep_enable_ext0_wakeup(SHUTTER, 0);
    esp_err_t statusWake = esp_sleep_enable_ext1_wakeup(1ULL << WAKE, ESP_EXT1_WAKEUP_ALL_LOW);
    if (shutterWake != ESP_OK || statusWake != ESP_OK) {
        Serial.printf("sleep_configuration_failed=%d,%d\n", shutterWake, statusWake);
        lastInteraction = millis();
        return;
    }
    gpio_hold_en(POWER_HOLD);
    gpio_hold_en(SENSOR_RESET);
    gpio_deep_sleep_hold_en();
    sleepingBoot = bootTag;
    sleepingAt = time(nullptr) > 1700000000 ? time(nullptr) : 0;
    sleepMarker = 0xCA6E2026;
    usbTestMode = false;
    Serial.println("sleep");
    Serial.flush();
    esp_deep_sleep_start();
}

void setup() {
    pinMode(POWER_HOLD, OUTPUT);
    digitalWrite(POWER_HOLD, HIGH);
    pinMode(SENSOR_RESET, OUTPUT);
    digitalWrite(SENSOR_RESET, LOW);
    gpio_hold_dis(POWER_HOLD);
    gpio_hold_dis(SENSOR_RESET);
    gpio_deep_sleep_hold_dis();
    rtc_gpio_deinit(SHUTTER);
    rtc_gpio_deinit(WAKE);
    pinMode(SHUTTER, INPUT_PULLUP);
    pinMode(WAKE, INPUT_PULLUP);
    pinMode(LED, OUTPUT);
    digitalWrite(LED, LOW);
    Serial.begin(115200);
    bootTag = esp_random();
    previousSleepConfirmed = esp_reset_reason() == ESP_RST_DEEPSLEEP && sleepMarker == 0xCA6E2026;
    if (previousSleepConfirmed) {
        time_t now = time(nullptr);
        if (sleepingAt > 1700000000 && now >= sleepingAt) sleepSeconds = difftime(now, sleepingAt);
        ++wakeCount;
    } else wakeCount = 0;
    sleepMarker = 0;
    WiFi.mode(WIFI_STA);
    identityReady = WiFi.macAddress().equalsIgnoreCase(CAMERA_ID);
    if (!identityReady) {
        Serial.println("identity_mismatch");
        WiFi.mode(WIFI_OFF);
        return;
    }
    storageReady = LittleFS.begin(false);
    if (storageReady) {
        File root = LittleFS.open("/");
        for (File entry = root.openNextFile(); entry; entry = root.openNextFile()) {
            String path = String("/") + entry.name();
            if (path.endsWith(".part") || path.endsWith(".meta") ||
                (path.endsWith(".jpg") && !LittleFS.exists(path.substring(0, path.length() - 4) + ".json")) ||
                (path.endsWith(".json") && !LittleFS.exists(path.substring(0, path.length() - 5) + ".jpg"))) {
                entry.close();
                LittleFS.remove(path);
            }
        }
    }
    status();
    bool wakingForStatus = esp_sleep_get_wakeup_cause() == ESP_SLEEP_WAKEUP_EXT1 ||
                           digitalRead(WAKE) == LOW;
    bool wakingForPhoto = esp_sleep_get_wakeup_cause() == ESP_SLEEP_WAKEUP_EXT0 && !wakingForStatus;
    trigger = wakingForStatus ? "wake_button" : wakingForPhoto ? "wake_shutter" : "boot";
    work(wakingForPhoto);
}

void loop() {
    if (!identityReady) { delay(100); return; }
    static char command[32];
    static size_t commandLength = 0;
    static bool commandOverflow = false;
    while (Serial.available()) {
        char character = (char)Serial.read();
        if (character == '\r') continue;
        if (character == '\n') {
            command[commandLength] = '\0';
            lastInteraction = millis();
            if (commandOverflow) Serial.println("command=TOO_LONG");
            else if (strcmp(command, "STATUS") == 0) status();
            else if (strcmp(command, "REPORT") == 0) { trigger = "usb_status"; work(false); status(); }
            else if (strcmp(command, "USB_TEST_ON") == 0) {
                usbTestMode = true;
                Serial.println("usb_test=on button_triggers_disabled_until_sleep");
            } else if (strcmp(command, "USB_TEST_OFF") == 0) {
                usbTestMode = false;
                Serial.println("usb_test=off");
            } else if (strcmp(command, "CAPTURE") == 0 || strcmp(command, "CAPTURE_SETTLED") == 0) {
                Serial.println("command=CAPTURE accepted");
                trigger = "usb_command";
                work(true);
            } else Serial.println("command=UNKNOWN_OR_NO_USB");
            commandLength = 0;
            commandOverflow = false;
        } else if (commandLength < sizeof(command) - 1) command[commandLength++] = character;
        else commandOverflow = true;
    }
    static bool shutterArmed = false, wakeArmed = false;
    static bool previousShutter = LOW, previousWake = LOW;
    static uint32_t shutterChanged = 0, wakeChanged = 0;
    uint32_t now = millis();
    bool shutterLevel = digitalRead(SHUTTER);
    bool wakeLevel = digitalRead(WAKE);
    if (shutterLevel != previousShutter) { previousShutter = shutterLevel; shutterChanged = now; }
    if (wakeLevel != previousWake) { previousWake = wakeLevel; wakeChanged = now; }
    if (now - wakeChanged >= 30) {
        if (wakeLevel == HIGH) wakeArmed = true;
        else if (wakeArmed) {
            wakeArmed = false;
            shutterArmed = false;
            trigger = "wake_button";
            feedback(1);
            work(false);
        }
    }
    if (now - shutterChanged >= 30) {
        if (shutterLevel == HIGH) shutterArmed = true;
        else if (shutterArmed) {
            shutterArmed = false;
            if (wakeLevel == HIGH && !usbTestMode) { trigger = "button"; work(true); }
        }
    }
    if (millis() - lastInteraction >= AWAKE_MS) sleepWhenReleased();
    delay(5);
}