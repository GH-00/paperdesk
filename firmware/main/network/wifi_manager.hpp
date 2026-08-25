#pragma once

#include <cstdint>

#include "esp_err.h"
#include "esp_event.h"
#include "esp_netif.h"
#include "freertos/FreeRTOS.h"
#include "freertos/event_groups.h"

namespace paperdesk {

class WifiManager {
public:
    explicit WifiManager(
        std::uint8_t max_retry_count = 5
    );

    ~WifiManager();

    WifiManager(const WifiManager&) = delete;
    WifiManager& operator=(const WifiManager&) = delete;

    esp_err_t initialize();

    esp_err_t connect(
        const char* ssid,
        const char* password
    );

    bool is_connected() const;

    esp_err_t disconnect();

private:
    static void event_handler(
        void* arg,
        esp_event_base_t event_base,
        int32_t event_id,
        void* event_data
    );

    void cleanup();

    std::uint8_t max_retry_count_;
    std::uint8_t retry_count_ = 0;
    bool initialized_ = false;
    bool wifi_started_ = false;
    bool wifi_initialized_ = false;
    bool nvs_initialized_ = false;
    bool netif_initialized_ = false;
    bool event_loop_created_ = false;

    esp_netif_t* netif_ = nullptr;
    EventGroupHandle_t event_group_ = nullptr;
    esp_event_handler_instance_t wifi_event_instance_ = nullptr;
    esp_event_handler_instance_t ip_event_instance_ = nullptr;
};

}