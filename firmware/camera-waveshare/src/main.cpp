#include <Arduino.h>
#include <atomic>
#include <ArduinoJson.h>
#include <HTTPClient.h>
#include <LittleFS.h>
#include <Preferences.h>
#include <WiFi.h>
#include <Wire.h>
#include <WiFiClientSecure.h>
#include <driver/rtc_io.h>
#include <esp_camera.h>
#include <esp_sleep.h>
#include <esp_system.h>
#include <soc/soc.h>
#include <soc/io_mux_reg.h>
#include <soc/gpio_reg.h>
#include <soc/usb_serial_jtag_reg.h>
#include <time.h>
#include <errno.h>
#include "camera_secrets.h"

static constexpr gpio_num_t BUTTON = GPIO_NUM_1;
static constexpr gpio_num_t BOOT_BUTTON = GPIO_NUM_0;
static constexpr gpio_num_t POWER_BUTTON = GPIO_NUM_15;
static constexpr int LED = 2;
static constexpr uint8_t EXPANDER = 0x24;
static uint8_t boardOutputs = (1 << 5) | (1 << 3);
static bool boardReady = false;
static bool audioAdcStandby = false;
static const char *FIRMWARE = "waveshare-2026-09-17-pwr-audio-sleep";
static int batterySchedule = -60;
static constexpr uint32_t NETWORK_MS = 20000;
static constexpr size_t MAX_JPEG = 750000;
static constexpr int QUEUE_LIMIT = 3;
static volatile bool busy = false;
static volatile int feedback = 0;
static std::atomic<bool> acquiring{false};
static bool storageReady = false;
static uint32_t bootTag;
static uint32_t lastUsb = 0;
static uint32_t lastFrame = 0;
static uint32_t lastAttempt = 0;
static const char *captureResult = "not_requested";
static bool usbTestMode = false;
static bool captureRequested = false;
static constexpr int WARMUP_FRAMES = 2;
static String captureId;
static String uploadId;
static const char *trigger = "boot";
static const char *networkResult = "not_attempted";
static uint32_t captureMs = 0, uploadMs = 0, workMs = 0;
static uint32_t sensorInitMs = 0, frameReadyMs = 0, storageMs = 0;
static size_t jpegBytes = 0, frameWidth = 0, frameHeight = 0;
static int uploadHttp = 0;
static bool uploadAccepted = false;
static bool sleepReportAttempted = false;
static bool previousSleepConfirmed = false;
static double sleepSeconds = -1;
static uint32_t previousBoot = 0;
static time_t previousSleepAt = 0;
RTC_DATA_ATTR static uint32_t sleepMarker = 0;
RTC_DATA_ATTR static uint32_t sleepingBoot = 0;
RTC_DATA_ATTR static time_t sleepingAt = 0;
RTC_DATA_ATTR static uint32_t wakeCount = 0;

static bool writeRegister(uint8_t device, uint8_t address, uint8_t value) {
    Wire.beginTransmission(device);
    Wire.write(address);
    Wire.write(value);
    return Wire.endTransmission() == 0;
}

static bool boardWrite(uint8_t address, uint8_t value) {
    return writeRegister(EXPANDER, address, value);
}

static bool readRegister(uint8_t device, uint8_t address, uint8_t &value) {
    Wire.beginTransmission(device);
    Wire.write(address);
    if (Wire.endTransmission(false) != 0) return false;
    if (Wire.requestFrom(device, (uint8_t)1) != 1) return false;
    value = Wire.read();
    return true;
}

static bool stopAudioAdc() {
    const uint8_t registers[][3] = {
        {0x47, 0xff, 0x3f}, {0x48, 0xff, 0x1f}, {0x49, 0xff, 0x3f},
        {0x4a, 0xff, 0x1f}, {0x4b, 0xff, 0xff}, {0x4c, 0xff, 0xff},
        {0x40, 0xc0, 0xc0}, {0x01, 0x7f, 0x7f}, {0x06, 0x07, 0x07},
    };
    bool success = true;
    for (const auto &entry : registers) {
        bool written = writeRegister(0x40, entry[0], entry[1]);
        success = written && success;
    }
    for (const auto &entry : registers) {
        uint8_t value = 0;
        bool verified = readRegister(0x40, entry[0], value) && value == entry[2];
        Serial.printf("audio_adc register=0x%02x value=0x%02x verified=%d\n",
                      entry[0], value, verified);
        if (!verified) Serial.printf("audio_adc_standby_failed register=0x%02x\n", entry[0]);
        success = verified && success;
    }
    return success;
}

static bool batteryRead(uint16_t &value) {
    if (!boardReady) return false;
    Wire.beginTransmission(EXPANDER);
    Wire.write(0x06);
    if (Wire.endTransmission(false) != 0) return false;
    if (Wire.requestFrom(EXPANDER, (uint8_t)2) != 2) return false;
    uint8_t low = Wire.read();
    uint8_t high = Wire.read();
    value = (uint16_t)high << 8 | low;
    return true;
}

static bool batteryVoltage(float &voltage, uint16_t &raw) {
    uint32_t total = 0;
    for (int sample = 0; sample < 8; ++sample) {
        uint16_t value;
        if (!batteryRead(value) || value == 0 || value >= 1023) return false;
        total += value;
        delay(2);
    }
    raw = (total + 4) / 8;
    voltage = total * (3.3f * 3.0f / (1023.0f * 8));
    return voltage >= 2.5f && voltage <= 4.5f;
}

static void acceptBatterySettings(const String &body) {
    StaticJsonDocument<256> settings;
    if (deserializeJson(settings, body) || !settings["received"].is<bool>() ||
        !settings["received"].as<bool>() || !settings["batteryStatusEnabled"].is<bool>() ||
        !settings["batteryStatusMinutes"].is<int>()) return;
    int minutes = settings["batteryStatusMinutes"];
    if (minutes < 1 || minutes > 1440) return;
    int schedule = settings["batteryStatusEnabled"].as<bool>() ? minutes : -minutes;
    if (schedule == batterySchedule) return;
    Preferences preferences;
    if (!preferences.begin("camera-power", false)) return;
    size_t written = preferences.putInt("schedule", schedule);
    preferences.end();
    if (written != sizeof(int32_t)) {
        Serial.println("battery_settings=storage_failed");
        return;
    }
    batterySchedule = schedule;
    Serial.printf("battery_settings=applied enabled=%d minutes=%d\n",
                  schedule > 0, abs(schedule));
}

static bool cameraStandby(bool standby) {
    if (standby) boardOutputs |= (1 << 3);
    else boardOutputs &= ~(1 << 3);
    bool success = boardWrite(0x03, boardOutputs);
    if (!success) {
        boardReady = false;
        Serial.println("board_error=expander_write");
    }
    return success;
}

static void stopCamera() {
    esp_camera_deinit();
    cameraStandby(true);
}

static void reportBoard() {
    if (!busy) {
        uint16_t batteryRaw = 0;
        float voltage = 0;
        bool batteryValid = batteryVoltage(voltage, batteryRaw);
        Serial.printf("battery_read=%d battery_raw=%u battery_voltage=%.3f scale=nominal\n",
                      batteryValid, batteryRaw, batteryValid ? voltage : -1);
        if (boardReady) {
            const uint8_t registers[][2] = {
                {0x18, 0x0d}, {0x18, 0x12}, {0x40, 0x01}, {0x40, 0x06},
                {0x40, 0x40}, {0x40, 0x47}, {0x40, 0x4b}, {0x40, 0x4c},
            };
            for (const auto &entry : registers) {
                uint8_t value = 0;
                bool valid = readRegister(entry[0], entry[1], value);
                Serial.printf("audio_power device=0x%02x register=0x%02x read=%d value=0x%02x\n",
                              entry[0], entry[1], valid, value);
            }
        }
    }
    Serial.printf("board=waveshare-ov5640 firmware=%s expander=%d outputs=0x%02x "
                  "button_gpio=%d led_gpio=%d boot_gpio=0 boot_released=%d\n",
                  FIRMWARE, boardReady, boardOutputs, (int)BUTTON, LED,
                  digitalRead(BOOT_BUTTON) == HIGH);
    Serial.printf("battery_updates=%d battery_interval_minutes=%d wake=%s\n",
                  batterySchedule > 0, abs(batterySchedule),
                  esp_sleep_get_wakeup_cause() == ESP_SLEEP_WAKEUP_TIMER ? "timer" : "manual");
    Serial.printf("pwr_gpio=%d pwr_released=%d input_only=1\n",
                  (int)POWER_BUTTON, digitalRead(POWER_BUTTON) == HIGH);
    Serial.printf("audio_adc_standby=%d\n", audioAdcStandby);
}

static const char *wakeCause() {
    switch (esp_sleep_get_wakeup_cause()) {
        case ESP_SLEEP_WAKEUP_EXT0: return "button";
        case ESP_SLEEP_WAKEUP_EXT1:
            return esp_sleep_get_ext1_wakeup_status() & (1ULL << BOOT_BUTTON)
                ? "boot_button" : "power_button";
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

static bool captureFailed(const char *reason) {
    captureResult = reason;
    Serial.printf("capture_failed=%s\n", reason);
    return false;
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

static void probeStorage() {
    Serial.printf("storage total=%u used=%u\n", LittleFS.totalBytes(), LittleFS.usedBytes());
    String prefix = "/probe-" + String(esp_random(), HEX);
    for (int length : {16, 37}) {
        String path = prefix;
        while (path.length() < length) path += "x";
        errno = 0;
        File probe = LittleFS.open(path, "w");
        int openedError = errno;
        size_t written = probe ? probe.write((const uint8_t *)"test", 4) : 0;
        Serial.printf("storage_probe length=%u opened=%d errno=%d written=%u\n",
                      path.length(), (bool)probe, openedError, written);
        if (probe) {
            probe.close();
            LittleFS.remove(path);
        }
    }
}

static bool capture() {
    if (!boardReady) return captureFailed("board_unavailable");
    if (!storageReady) return captureFailed("filesystem_unavailable");
    if (queued() >= QUEUE_LIMIT) return captureFailed("queue_full");
    Serial.printf("capture_started psram=%u free_heap=%u\n", ESP.getPsramSize(), ESP.getFreeHeap());
    uint32_t capturedMillis = millis();
    time_t capturedEpoch = time(nullptr);
    camera_config_t config = {};
    config.ledc_channel = LEDC_CHANNEL_0;
    config.ledc_timer = LEDC_TIMER_0;
    config.pin_d0 = 45; config.pin_d1 = 47; config.pin_d2 = 48; config.pin_d3 = 46;
    config.pin_d4 = 42; config.pin_d5 = 40; config.pin_d6 = 39; config.pin_d7 = 21;
    config.pin_xclk = 38; config.pin_pclk = 41;
    config.pin_vsync = 17; config.pin_href = 18;
    config.pin_sccb_sda = -1; config.pin_sccb_scl = -1;
    config.sccb_i2c_port = 0;
    config.pin_pwdn = -1; config.pin_reset = -1;
    config.xclk_freq_hz = 20000000;
    config.pixel_format = PIXFORMAT_JPEG;
    config.frame_size = FRAMESIZE_UXGA;
    config.jpeg_quality = 12;
    config.fb_count = 1;
    config.fb_location = CAMERA_FB_IN_PSRAM;
    config.grab_mode = CAMERA_GRAB_WHEN_EMPTY;
    if (!psramFound()) return captureFailed("psram_unavailable");
    if (!cameraStandby(false)) return captureFailed("camera_power");
    delay(20);
    esp_err_t initialized = esp_camera_init(&config);
    sensorInitMs = millis() - capturedMillis;
    if (initialized != ESP_OK) {
        Serial.printf("camera_init_error=0x%x\n", initialized);
        cameraStandby(true);
        return captureFailed("sensor_initialization");
    }
    sensor_t *sensor = esp_camera_sensor_get();
    if (!sensor || sensor->id.PID != OV5640_PID) {
        stopCamera();
        return captureFailed("unexpected_sensor");
    }
    if (sensor->set_exposure_ctrl(sensor, 1) != 0 ||
        sensor->set_gain_ctrl(sensor, 1) != 0 || sensor->set_whitebal(sensor, 1) != 0) {
        stopCamera();
        return captureFailed("automatic_controls");
    }
    Serial.printf("sensor=%04x psram=%u aec=%u agc=%u awb=%u warmup_frames=%d\n",
                  sensor->id.PID, ESP.getPsramSize(), sensor->status.aec,
                  sensor->status.agc, sensor->status.awb, WARMUP_FRAMES);
    for (int frame = 0; frame < WARMUP_FRAMES; ++frame) {
        camera_fb_t *warmup = esp_camera_fb_get();
        if (!warmup) {
            stopCamera();
            return captureFailed("warmup_frame");
        }
        esp_camera_fb_return(warmup);
        delay(80);
    }
    camera_fb_t *image = esp_camera_fb_get();
    frameReadyMs = millis() - capturedMillis;
    acquiring.store(false);
    uint32_t storageBegan = millis();
    Serial.printf("capture_timing sensor_init_ms=%u frame_ready_ms=%u\n",
                  sensorInitMs, frameReadyMs);
    if (image) {
        jpegBytes = image->len;
        frameWidth = image->width;
        frameHeight = image->height;
    }
    if (!image) Serial.println("frame=null");
    else Serial.printf("frame width=%u height=%u format=%d bytes=%u\n",
                       image->width, image->height, image->format, image->len);
    bool saved = false;
    if (image && image->format == PIXFORMAT_JPEG && image->width == 1600 &&
        image->height == 1200 && image->len > 4 && image->len <= MAX_JPEG &&
        image->buf[0] == 0xff && image->buf[1] == 0xd8) {
        String id;
        String path;
        do {
            id = identifier();
            path = queuePath(id);
        } while (LittleFS.exists(path + ".json") || LittleFS.exists(path + ".jpg") ||
                 LittleFS.exists(path + ".part") || LittleFS.exists(path + ".meta"));
        captureId = id;
        File temporary = LittleFS.open(path + ".part", "w");
        if (!temporary) Serial.printf("capture_open_errno=%d total=%u used=%u\n",
                           errno, LittleFS.totalBytes(), LittleFS.usedBytes());
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
    stopCamera();
    if (!saved) return captureFailed("frame_or_storage");
    captureResult = "saved";
    return saved;
}

static bool connectForReport() {
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
    {
        WiFiClientSecure tls;
        tls.setCACert(HUB_CA);
        tls.setHandshakeTimeout(10);
        HTTPClient http;
        http.setConnectTimeout(5000);
        http.setTimeout(10000);
        if (http.begin(tls, String(HUB_URL) + "/status")) {
            StaticJsonDocument<2048> status;
            status["usb"] = millis() - lastUsb < 2000;
            status["board"] = "waveshare-ov5640";
            status["batteryStatusEnabled"] = batterySchedule > 0;
            status["batteryStatusMinutes"] = abs(batterySchedule);
            status["voltage"] = nullptr;
            uint16_t batteryRaw = 0;
            float voltage = 0;
            if (batteryVoltage(voltage, batteryRaw)) {
                status["voltage"] = voltage;
            }
            status["rssi"] = WiFi.RSSI();
            status["firmware"] = FIRMWARE;
            status["captureResult"] = captureResult;
            status["queued"] = storageReady ? queued() : -1;
            JsonObject diagnostics = status.createNestedObject("diagnostics");
            diagnostics["captureRequested"] = captureRequested;
            diagnostics["phase"] = phase;
            diagnostics["bootId"] = String(bootTag, HEX);
            diagnostics["previousBootId"] = String(previousBoot, HEX);
            diagnostics["wakeCause"] = wakeCause();
            diagnostics["resetReason"] = resetReason();
            diagnostics["resetCode"] = (int)esp_reset_reason();
            diagnostics["previousSleepConfirmed"] = previousSleepConfirmed;
            diagnostics["previousSleepAt"] = (long long)previousSleepAt;
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
            diagnostics["usb"] = millis() - lastUsb < 2000;
            diagnostics["buttonPressed"] = digitalRead(BUTTON) == LOW;
            diagnostics["clockSet"] = time(nullptr) >= 1700000000;
            http.addHeader("Authorization", String("Bearer ") + CAMERA_TOKEN);
            http.addHeader("X-Camera-Id", WiFi.macAddress());
            http.addHeader("Content-Type", "application/json");
            String body;
            serializeJson(status, body);
            Serial.printf("diagnostics=%s\n", body.c_str());
            int response = http.POST(body);
            Serial.printf("status_http=%d phase=%s\n", response, phase);
            if (response == 200) acceptBatterySettings(http.getString());
            http.end();
        }
    }
}

static bool deliver() {
    if (!connectForReport()) return false;
    reportStatus("before_upload");
    File root = LittleFS.open("/");
    for (File entry = root.openNextFile(); entry; entry = root.openNextFile()) {
        if (!String(entry.name()).endsWith(".json")) continue;
        StaticJsonDocument<256> record;
        DeserializationError parseError = deserializeJson(record, entry);
        if (parseError) {
            Serial.printf("queue_parse_error=%s file=%s\n", parseError.c_str(), entry.name());
            continue;
        }
        entry.close();
        String id = record["id"].as<String>();
        String path = queuePath(id);
        File image = LittleFS.open(path + ".jpg", "r");
        if (!image || image.size() == 0) {
            Serial.printf("queued_image_missing=%s\n", id.c_str());
            continue;
        }
        WiFiClientSecure tls;
        tls.setCACert(HUB_CA);
        tls.setHandshakeTimeout(10);
        HTTPClient http;
        http.setConnectTimeout(5000);
        http.setTimeout(15000);
        if (!http.begin(tls, String(HUB_URL) + "/photos/" + id)) return false;
        http.addHeader("Authorization", String("Bearer ") + CAMERA_TOKEN);
        http.addHeader("Content-Type", "image/jpeg");
        http.addHeader("X-Camera-Id", WiFi.macAddress());
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
        if (!accepted) return false;
        if (!LittleFS.remove(path + ".json")) {
            Serial.printf("receipt_cleanup_failed=%s\n", id.c_str());
            return false;
        }
        LittleFS.remove(path + ".jpg");
        while (feedback != 0) delay(20);
        feedback = 2;
        while (feedback != 0) delay(20);
    }
    return true;
}

static void work(void *argument) {
    uint32_t workBegan = millis();
    workMs = 0;
    bool takePhoto = argument == (void *)1;
    captureRequested = takePhoto;
    bool sleepOnly = argument == (void *)2;
    bool batteryOnly = argument == (void *)3;
    if (takePhoto) {
        captureResult = "started";
        captureId = ""; uploadId = "";
        jpegBytes = 0; frameWidth = 0; frameHeight = 0;
        uploadHttp = 0; uploadMs = 0; uploadAccepted = false;
        sensorInitMs = 0; frameReadyMs = 0; storageMs = 0;
        uint32_t captureBegan = millis();
        bool captured = capture();
        acquiring.store(false);
        captureMs = millis() - captureBegan;
        if (!captured) {
            while (feedback != 0) delay(20);
            feedback = 3;
            while (feedback != 0) delay(20);
        }
    }
    WiFi.mode(WIFI_STA);
    WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
    if (batteryOnly) {
        connectForReport();
        workMs = millis() - workBegan;
        reportStatus("battery_update");
    }
    else if (sleepOnly) connectForReport();
    else {
        if (storageReady) deliver();
        else connectForReport();
        workMs = millis() - workBegan;
        reportStatus("operation_complete");
    }
    if (millis() - lastUsb >= 2000 && digitalRead(BUTTON) == HIGH &&
        digitalRead(POWER_BUTTON) == HIGH) {
        reportStatus("sleep_planned");
        sleepReportAttempted = true;
    }
    WiFi.disconnect(true);
    WiFi.mode(WIFI_OFF);
    lastAttempt = millis();
    busy = false;
    vTaskDelete(nullptr);
}

static void startWork(bool takePhoto, bool sleepOnly = false, bool batteryOnly = false) {
    busy = true;
    if (takePhoto) {
        acquiring.store(true);
        feedback = 1;
        digitalWrite(LED, HIGH);
    }
    if (xTaskCreatePinnedToCore(work, "camera", 16384,
                               batteryOnly ? (void *)3 : sleepOnly ? (void *)2 :
                                   takePhoto ? (void *)1 : nullptr,
                               1, nullptr, 0) != pdPASS) {
        busy = false;
        acquiring.store(false);
        digitalWrite(LED, LOW);
        if (sleepOnly) sleepReportAttempted = true;
        feedback = 3;
    }
}

void setup() {
    rtc_gpio_deinit(BOOT_BUTTON);
    pinMode(BOOT_BUTTON, INPUT_PULLUP);
    rtc_gpio_deinit(POWER_BUTTON);
    pinMode(POWER_BUTTON, INPUT_PULLUP);
    rtc_gpio_deinit(BUTTON);
    pinMode(BUTTON, INPUT_PULLUP);
    pinMode(LED, OUTPUT);
    digitalWrite(LED, LOW);
    Serial.begin(115200);
    Preferences preferences;
    if (preferences.begin("camera-power", true)) {
        int schedule = preferences.getInt("schedule", -60);
        if ((schedule >= 1 && schedule <= 1440) || (schedule <= -1 && schedule >= -1440)) {
            batterySchedule = schedule;
        }
        preferences.end();
    }
    uint8_t mac[6];
    esp_read_mac(mac, ESP_MAC_WIFI_STA);
    char identity[18];
    snprintf(identity, sizeof(identity), "%02X:%02X:%02X:%02X:%02X:%02X",
             mac[0], mac[1], mac[2], mac[3], mac[4], mac[5]);
    if (strcmp(identity, CAMERA_ID) != 0) {
        while (true) { Serial.println("identity_mismatch"); delay(1000); }
    }
    boardReady = Wire.begin(8, 7, 100000);
    Wire.setTimeOut(100);
    boardReady = boardReady && boardWrite(0x03, boardOutputs) && boardWrite(0x02, 0x7f);
    audioAdcStandby = boardReady && stopAudioAdc();
    reportBoard();
    bootTag = esp_random();
    previousSleepConfirmed = esp_reset_reason() == ESP_RST_DEEPSLEEP && sleepMarker == 0xCA6E2026;
    if (previousSleepConfirmed) {
        previousBoot = sleepingBoot;
        previousSleepAt = sleepingAt;
        time_t now = time(nullptr);
        if (sleepingAt > 1700000000 && now >= sleepingAt) sleepSeconds = difftime(now, sleepingAt);
        ++wakeCount;
    } else wakeCount = 0;
    sleepMarker = 0;
    lastUsb = millis();
    storageReady = LittleFS.begin(false);
    if (storageReady) {
        File root = LittleFS.open("/");
        for (File entry = root.openNextFile(); entry; entry = root.openNextFile()) {
            String path = String("/") + entry.name();
            if (path.endsWith(".part") || path.endsWith(".meta") ||
                (path.endsWith(".jpg") && !LittleFS.exists(path.substring(0, path.length() - 4) + ".json")) ||
                (path.endsWith(".json") && !LittleFS.exists(path.substring(0, path.length() - 5) + ".jpg"))) {
                Serial.printf("queue_incomplete=%s\n", path.c_str());
                entry.close();
                LittleFS.remove(path);
            }
        }
    }
    Serial.printf("camera ready filesystem=%d wake=%d\n", storageReady, esp_sleep_get_wakeup_cause());
    if (esp_sleep_get_wakeup_cause() == ESP_SLEEP_WAKEUP_EXT0) {
        trigger = "wake_button";
        startWork(true);
    } else if (esp_sleep_get_wakeup_cause() == ESP_SLEEP_WAKEUP_EXT1) {
        bool bootPressed = esp_sleep_get_ext1_wakeup_status() & (1ULL << BOOT_BUTTON);
        trigger = bootPressed ? "wake_boot" : "wake_power_button";
        startWork(!bootPressed);
    } else if (esp_sleep_get_wakeup_cause() == ESP_SLEEP_WAKEUP_TIMER) {
        trigger = "battery_timer";
        startWork(false, false, true);
    } else if (esp_sleep_get_wakeup_cause() == ESP_SLEEP_WAKEUP_UNDEFINED) {
        startWork(false);
    }
}

void loop() {
    uint32_t now = millis();
    uint32_t frame = REG_READ(USB_SERIAL_JTAG_FRAM_NUM_REG);
    if (frame != lastFrame) { lastUsb = now; lastFrame = frame; }
    static int activeFeedback = 0;
    static uint32_t feedbackBegan = 0;
    static uint32_t lastDark = 0;
    if (!activeFeedback && feedback && (feedback == 1 || now - lastDark >= 500)) {
        activeFeedback = feedback;
        feedbackBegan = now;
    }
    if (activeFeedback == 1) {
        if (!acquiring.load()) {
            digitalWrite(LED, LOW);
            Serial.printf("capture_light=off frame_ready_ms=%u\n", frameReadyMs);
            if (feedback == 1) feedback = 0;
            activeFeedback = 0;
            lastDark = now;
        }
    } else if (activeFeedback) {
        uint32_t elapsed = now - feedbackBegan;
        digitalWrite(LED, elapsed / 150 % 2 == 0 && elapsed < activeFeedback * 300 - 150);
        if (elapsed >= activeFeedback * 300) {
            digitalWrite(LED, LOW);
            if (feedback == activeFeedback) feedback = 0;
            activeFeedback = 0;
            lastDark = now;
        }
    }
    static bool previous = LOW;
    static bool stable = LOW;
    static bool armed = false;
    static uint32_t changed = 0;
    static bool bootPrevious = LOW;
    static bool bootStable = LOW;
    static bool bootArmed = false;
    static bool restartRequested = false;
    static uint32_t bootChanged = 0;
    bool bootLevel = digitalRead(BOOT_BUTTON);
    if (bootLevel != bootPrevious) { bootPrevious = bootLevel; bootChanged = now; }
    if (now - bootChanged >= 30 && bootStable != bootLevel) {
        bootStable = bootLevel;
        if (bootStable == HIGH) bootArmed = true;
        else if (bootArmed) {
            restartRequested = true;
            bootArmed = false;
        }
    }
    if (restartRequested && bootStable == HIGH && !busy && !feedback && !activeFeedback) {
        Serial.println("restart=boot_button_released");
        Serial.flush();
        esp_restart();
    }
    bool powerReleased = digitalRead(POWER_BUTTON) == HIGH;
    bool pressed = digitalRead(BUTTON) == HIGH && powerReleased;
    if (pressed != previous) { previous = pressed; changed = now; }
    if (now - changed >= 30 && stable != pressed) {
        stable = pressed;
        if (stable == HIGH) armed = true;
        else {
            if (armed && !busy && !feedback && !activeFeedback && !usbTestMode) {
                trigger = powerReleased ? "button" : "power_button";
                startWork(true);
            }
            armed = false;
        }
    }
    bool usb = now - lastUsb < 2000;
    if (!usb) usbTestMode = false;
    if (usb) sleepReportAttempted = false;
    static char command[32];
    static size_t commandLength = 0;
    while (Serial.available()) {
        char character = (char)Serial.read();
        if (character == '\r') continue;
        if (character == '\n') {
            command[commandLength] = '\0';
            if (strcmp(command, "USB_TEST_ON") == 0 && usb) {
                usbTestMode = true;
                Serial.println("usb_test=on button_triggers_disabled_until_disconnect");
            } else if (strcmp(command, "USB_TEST_OFF") == 0) {
                usbTestMode = false;
                Serial.println("usb_test=off");
            } else if ((strcmp(command, "CAPTURE") == 0 ||
                        strcmp(command, "CAPTURE_SETTLED") == 0) && usb) {
                if (busy || feedback || activeFeedback) Serial.println("command=BUSY");
                else {
                    Serial.println("command=CAPTURE accepted");
                    trigger = "usb_command";
                    startWork(true);
                }
            } else if (strcmp(command, "STATUS") == 0) {
                reportBoard();
                Serial.printf("led_gpio=%d output_enabled=%d level=%d\n", LED,
                              (REG_READ(GPIO_ENABLE_REG) & (1UL << LED)) != 0,
                              (REG_READ(GPIO_OUT_REG) & (1UL << LED)) != 0);
                uint32_t buttonMux = REG_READ(IO_MUX_GPIO1_REG);
                Serial.printf("button_gpio=%d raw=%d pullup=%d pulldown=%d input_enabled=%d output_enabled=%d mux=0x%lx\n",
                              (int)BUTTON, digitalRead(BUTTON), (buttonMux & FUN_PU) != 0,
                              (buttonMux & FUN_PD) != 0, (buttonMux & FUN_IE) != 0,
                              (REG_READ(GPIO_ENABLE_REG) & (1UL << BUTTON)) != 0,
                              (unsigned long)buttonMux);
                Serial.printf("status usb=%d busy=%d psram=%u filesystem=%d queued=%d last_capture=%s identity=%s button_gpio=%d usb_test=%d\n",
                              usb, busy, ESP.getPsramSize(), storageReady,
                              (!busy && storageReady) ? queued() : -1, captureResult,
                              WiFi.macAddress().c_str(), (int)BUTTON, usbTestMode);
            } else if (strcmp(command, "STORAGE") == 0 && usb && !busy && storageReady) {
                probeStorage();
            } else Serial.println("command=UNKNOWN_OR_NO_USB");
            commandLength = 0;
        } else if (commandLength < sizeof(command) - 1) command[commandLength++] = character;
        else commandLength = 0;
    }
    static uint32_t lastStatus = 0;
    if (usb && now - lastStatus >= 5000) {
        Serial.printf("usb=%d button=%d busy=%d filesystem=%d queued=%d led_gpio=%d\n",
                      usb, stable, busy, storageReady, (!busy && storageReady) ? queued() : -1, LED);
        lastStatus = now;
    }
    if (!busy && !feedback && !activeFeedback) {
        if (!usb && stable == HIGH && bootStable == HIGH && now > 5000 && boardReady) {
            if (!sleepReportAttempted) {
                startWork(false, true);
                return;
            }
            if (!cameraStandby(true)) return;
            rtc_gpio_pullup_en(BUTTON);
            rtc_gpio_pulldown_dis(BUTTON);
            rtc_gpio_pullup_en(BOOT_BUTTON);
            rtc_gpio_pulldown_dis(BOOT_BUTTON);
            rtc_gpio_pullup_en(POWER_BUTTON);
            rtc_gpio_pulldown_dis(POWER_BUTTON);
            if (esp_sleep_enable_ext0_wakeup(BUTTON, 0) != ESP_OK ||
                esp_sleep_enable_ext1_wakeup((1ULL << BOOT_BUTTON) | (1ULL << POWER_BUTTON),
                                             ESP_EXT1_WAKEUP_ANY_LOW) != ESP_OK) {
                Serial.println("sleep_error=wake_configuration");
                delay(1000);
                return;
            }
            esp_sleep_disable_wakeup_source(ESP_SLEEP_WAKEUP_TIMER);
            if (batterySchedule > 0 &&
                esp_sleep_enable_timer_wakeup((uint64_t)batterySchedule * 60ULL * 1000000ULL)
                    != ESP_OK) {
                Serial.println("sleep_error=timer_configuration");
                delay(1000);
                return;
            }
            sleepingBoot = bootTag;
            sleepingAt = time(nullptr) > 1700000000 ? time(nullptr) : 0;
            sleepMarker = 0xCA6E2026;
            Serial.println("sleep");
            Serial.flush();
            esp_deep_sleep_start();
        }
        if (usb && now - lastAttempt > 60000) startWork(false);
    }
    delay(5);
}