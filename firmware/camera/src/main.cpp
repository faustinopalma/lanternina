#include <Arduino.h>
#include <ArduinoJson.h>
#include <HTTPClient.h>
#include <LittleFS.h>
#include <WiFi.h>
#include <WiFiClientSecure.h>
#include <driver/rtc_io.h>
#include <esp_camera.h>
#include <esp_sleep.h>
#include <soc/soc.h>
#include <soc/usb_serial_jtag_reg.h>
#include <time.h>
#include "camera_secrets.h"

static constexpr gpio_num_t BUTTON = GPIO_NUM_4;
static constexpr int LED = 3;
static constexpr uint32_t NETWORK_MS = 20000;
static constexpr size_t MAX_JPEG = 750000;
static constexpr int QUEUE_LIMIT = 3;
static volatile bool busy = false;
static volatile int feedback = 0;
static bool storageReady = false;
static uint32_t bootTag;
static uint32_t lastUsb = 0;
static uint32_t lastFrame = 0;
static uint32_t lastAttempt = 0;

static String identifier() {
    char value[33];
    snprintf(value, sizeof(value), "%08lx%08lx%08lx%08lx",
             (unsigned long)esp_random(), (unsigned long)esp_random(),
             (unsigned long)esp_random(), (unsigned long)esp_random());
    return String(value);
}

static int queued() {
    int count = 0;
    File root = LittleFS.open("/");
    for (File entry = root.openNextFile(); entry; entry = root.openNextFile()) {
        if (String(entry.name()).endsWith(".json")) ++count;
    }
    return count;
}

static bool capture() {
    if (!storageReady || queued() >= QUEUE_LIMIT) return false;
    uint32_t capturedMillis = millis();
    time_t capturedEpoch = time(nullptr);
    camera_config_t config = {};
    config.ledc_channel = LEDC_CHANNEL_0;
    config.ledc_timer = LEDC_TIMER_0;
    config.pin_d0 = 15; config.pin_d1 = 17; config.pin_d2 = 18; config.pin_d3 = 16;
    config.pin_d4 = 14; config.pin_d5 = 12; config.pin_d6 = 11; config.pin_d7 = 48;
    config.pin_xclk = 10; config.pin_pclk = 13;
    config.pin_vsync = 38; config.pin_href = 47;
    config.pin_sccb_sda = 40; config.pin_sccb_scl = 39;
    config.pin_pwdn = -1; config.pin_reset = -1;
    config.xclk_freq_hz = 20000000;
    config.pixel_format = PIXFORMAT_JPEG;
    config.frame_size = FRAMESIZE_UXGA;
    config.jpeg_quality = 12;
    config.fb_count = 1;
    config.fb_location = CAMERA_FB_IN_PSRAM;
    config.grab_mode = CAMERA_GRAB_WHEN_EMPTY;
    if (!psramFound() || esp_camera_init(&config) != ESP_OK) return false;
    Serial.printf("sensor=%04x psram=%u\n", esp_camera_sensor_get()->id.PID, ESP.getPsramSize());
    for (int frame = 0; frame < 2; ++frame) {
        camera_fb_t *warmup = esp_camera_fb_get();
        if (warmup) esp_camera_fb_return(warmup);
        delay(80);
    }
    camera_fb_t *image = esp_camera_fb_get();
    bool saved = false;
    if (image && image->format == PIXFORMAT_JPEG && image->len <= MAX_JPEG) {
        String id = identifier();
        String path = "/" + id;
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
    if (image) esp_camera_fb_return(image);
    esp_camera_deinit();
    return saved;
}

static bool deliver() {
    uint32_t began = millis();
    while (WiFi.status() != WL_CONNECTED && millis() - began < NETWORK_MS) delay(50);
    if (WiFi.status() != WL_CONNECTED) return false;
    configTime(0, 0, "pool.ntp.org");
    began = millis();
    while (time(nullptr) < 1700000000 && millis() - began < 10000) delay(50);
    if (time(nullptr) < 1700000000) return false;
    {
        WiFiClientSecure tls;
        tls.setCACert(HUB_CA);
        tls.setHandshakeTimeout(10);
        HTTPClient http;
        http.setConnectTimeout(5000);
        http.setTimeout(10000);
        if (http.begin(tls, String(HUB_URL) + "/status")) {
            StaticJsonDocument<256> status;
            status["usb"] = millis() - lastUsb < 2000;
            status["voltage"] = nullptr;
#ifdef CAMERA_BATTERY_GPIO
            analogSetPinAttenuation(CAMERA_BATTERY_GPIO, ADC_11db);
            uint32_t millivolts = 0;
            for (int sample = 0; sample < 16; ++sample) {
                millivolts += analogReadMilliVolts(CAMERA_BATTERY_GPIO);
                delay(2);
            }
            status["voltage"] = millivolts * 2.0f / 16000.0f;
#endif
            status["rssi"] = WiFi.RSSI();
            status["firmware"] = "camera-2026-09-09";
            http.addHeader("Authorization", String("Bearer ") + CAMERA_TOKEN);
            http.addHeader("X-Camera-Id", WiFi.macAddress());
            http.addHeader("Content-Type", "application/json");
            String body;
            serializeJson(status, body);
            Serial.printf("status_http=%d\n", http.POST(body));
            http.end();
        }
    }
    File root = LittleFS.open("/");
    for (File entry = root.openNextFile(); entry; entry = root.openNextFile()) {
        if (!String(entry.name()).endsWith(".json")) continue;
        StaticJsonDocument<256> record;
        if (deserializeJson(record, entry)) continue;
        String id = record["id"].as<String>();
        File image = LittleFS.open("/" + id + ".jpg", "r");
        if (!image || image.size() == 0) continue;
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
        if (record["epoch"].as<long long>() > 1700000000) {
            http.addHeader("X-Captured-At", String(record["epoch"].as<long long>()));
        } else if (record["boot"].as<uint32_t>() == bootTag) {
            http.addHeader("X-Capture-Age", String((millis() - record["millis"].as<uint32_t>()) / 1000));
        }
        int status = http.sendRequest("PUT", &image, image.size());
        image.close();
        StaticJsonDocument<256> receipt;
        bool accepted = status == 201 || status == 200;
        accepted = accepted && !deserializeJson(receipt, http.getString());
        accepted = accepted && receipt["id"].as<String>() == id && receipt["stored"] == true;
        http.end();
        Serial.printf("upload=%s status=%d accepted=%d\n", id.c_str(), status, accepted);
        if (!accepted) return false;
        LittleFS.remove("/" + id + ".json");
        LittleFS.remove("/" + id + ".jpg");
        while (feedback != 0) delay(20);
        feedback = 2;
        while (feedback != 0) delay(20);
    }
    return true;
}

static void work(void *argument) {
    bool takePhoto = argument != nullptr;
    WiFi.mode(WIFI_STA);
    WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
    if (takePhoto && !capture()) {
        while (feedback != 0) delay(20);
        feedback = 3;
        while (feedback != 0) delay(20);
    }
    if (storageReady) deliver();
    WiFi.disconnect(true);
    WiFi.mode(WIFI_OFF);
    lastAttempt = millis();
    busy = false;
    vTaskDelete(nullptr);
}

static void startWork(bool takePhoto) {
    busy = true;
    if (xTaskCreatePinnedToCore(work, "camera", 16384,
                               takePhoto ? (void *)1 : nullptr, 1, nullptr, 0) != pdPASS) {
        busy = false;
        feedback = 3;
    }
}

void setup() {
    rtc_gpio_deinit(BUTTON);
    pinMode(BUTTON, INPUT_PULLUP);
    pinMode(LED, OUTPUT);
    digitalWrite(LED, LOW);
    Serial.begin(115200);
    bootTag = esp_random();
    lastUsb = millis();
    storageReady = LittleFS.begin(false);
    if (storageReady) {
        File root = LittleFS.open("/");
        for (File entry = root.openNextFile(); entry; entry = root.openNextFile()) {
            String path = String("/") + entry.name();
            if (path.endsWith(".part") || path.endsWith(".meta") ||
                (path.endsWith(".jpg") && !LittleFS.exists(path.substring(0, path.length() - 4) + ".json"))) {
                entry.close();
                LittleFS.remove(path);
            }
        }
    }
    Serial.printf("camera ready filesystem=%d wake=%d\n", storageReady, esp_sleep_get_wakeup_cause());
    if (esp_sleep_get_wakeup_cause() == ESP_SLEEP_WAKEUP_EXT0) {
        feedback = 1;
        startWork(true);
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
    if (!activeFeedback && feedback && now - lastDark >= 500) {
        activeFeedback = feedback;
        feedbackBegan = now;
    }
    if (activeFeedback) {
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
    bool pressed = digitalRead(BUTTON);
    if (pressed != previous) { previous = pressed; changed = now; }
    if (now - changed >= 30 && stable != pressed) {
        stable = pressed;
        if (stable == HIGH) armed = true;
        else {
            if (armed && !busy && !feedback && !activeFeedback) {
                feedback = 1;
                startWork(true);
            }
            armed = false;
        }
    }
    bool usb = now - lastUsb < 2000;
    static uint32_t lastStatus = 0;
    if (usb && now - lastStatus >= 5000) {
        Serial.printf("usb=%d button=%d busy=%d filesystem=%d queued=%d led_gpio=%d\n",
                      usb, stable, busy, storageReady, (!busy && storageReady) ? queued() : -1, LED);
        lastStatus = now;
    }
    if (!busy && !feedback && !activeFeedback && stable == HIGH) {
        if (!usb && now > 5000) {
            rtc_gpio_pullup_en(BUTTON);
            rtc_gpio_pulldown_dis(BUTTON);
            esp_sleep_enable_ext0_wakeup(BUTTON, 0);
            Serial.println("sleep");
            Serial.flush();
            esp_deep_sleep_start();
        }
        if (usb && now - lastAttempt > 60000) startWork(false);
    }
    delay(5);
}