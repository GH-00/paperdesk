#include "wifi_manager.hpp"

#include <cstring>

#include "esp_event.h"
#include "esp_log.h"
#include "esp_netif.h"
#include "esp_wifi.h"
#include "freertos/event_groups.h"
#include "nvs_flash.h"


namespace {


constexpr const char* TAG =
    "WifiManager";

constexpr EventBits_t WIFI_CONNECTED_BIT =
    BIT0;

constexpr EventBits_t WIFI_FAILED_BIT =
    BIT1;


}


namespace paperdesk {


WifiManager::WifiManager(
    std::uint8_t max_retry_count
)
    : max_retry_count_(
        max_retry_count
    )
{
}


WifiManager::~WifiManager()
{
    cleanup();
}


esp_err_t WifiManager::initialize()
{
    if (initialized_) {
        return ESP_OK;
    }

    esp_err_t result =
        nvs_flash_init();

    if (
        result == ESP_ERR_NVS_NO_FREE_PAGES
        || result == ESP_ERR_NVS_NEW_VERSION_FOUND
    ) {
        result =
            nvs_flash_erase();

        if (result == ESP_OK) {
            result =
                nvs_flash_init();
        }
    }

    if (
        result != ESP_OK
        && result != ESP_ERR_INVALID_STATE
    ) {
        ESP_LOGE(
            TAG,
            "NVS initialization failed: %s",
            esp_err_to_name(result)
        );

        return result;
    }

    nvs_initialized_ =
        result == ESP_OK;

    result =
        esp_netif_init();

    if (
        result != ESP_OK
        && result != ESP_ERR_INVALID_STATE
    ) {
        cleanup();
        return result;
    }

    netif_initialized_ =
        result == ESP_OK;

    result =
        esp_event_loop_create_default();

    if (
        result != ESP_OK
        && result != ESP_ERR_INVALID_STATE
    ) {
        cleanup();
        return result;
    }

    event_loop_created_ =
        result == ESP_OK;

    netif_ =
        esp_netif_create_default_wifi_sta();

    if (netif_ == nullptr) {
        cleanup();
        return ESP_ERR_NO_MEM;
    }

    wifi_init_config_t wifi_init_config =
        WIFI_INIT_CONFIG_DEFAULT();

    result =
        esp_wifi_init(
            &wifi_init_config
        );

    if (result != ESP_OK) {
        cleanup();
        return result;
    }

    wifi_initialized_ = true;

    result =
        esp_wifi_set_mode(
            WIFI_MODE_STA
        );

    if (result != ESP_OK) {
        cleanup();
        return result;
    }

    event_group_ =
        xEventGroupCreate();

    if (event_group_ == nullptr) {
        cleanup();
        return ESP_ERR_NO_MEM;
    }

    result =
        esp_event_handler_instance_register(
            WIFI_EVENT,
            ESP_EVENT_ANY_ID,
            &WifiManager::event_handler,
            this,
            reinterpret_cast<esp_event_handler_instance_t*>(
                &wifi_event_instance_
            )
        );

    if (result != ESP_OK) {
        cleanup();
        return result;
    }

    result =
        esp_event_handler_instance_register(
            IP_EVENT,
            IP_EVENT_STA_GOT_IP,
            &WifiManager::event_handler,
            this,
            reinterpret_cast<esp_event_handler_instance_t*>(
                &ip_event_instance_
            )
        );

    if (result != ESP_OK) {
        cleanup();
        return result;
    }

    initialized_ = true;

    ESP_LOGI(
        TAG,
        "Wi-Fi manager initialized in STA mode"
    );

    return ESP_OK;
}


esp_err_t WifiManager::connect(
    const char* ssid,
    const char* password
)
{
    if (
        !initialized_
        || ssid == nullptr
        || password == nullptr
        || std::strlen(ssid) >= sizeof(wifi_config_t::sta.ssid)
        || std::strlen(password) >= sizeof(wifi_config_t::sta.password)
    ) {
        return ESP_ERR_INVALID_ARG;
    }

    wifi_config_t config = {};

    std::strncpy(
        reinterpret_cast<char*>(config.sta.ssid),
        ssid,
        sizeof(config.sta.ssid) - 1
    );

    std::strncpy(
        reinterpret_cast<char*>(config.sta.password),
        password,
        sizeof(config.sta.password) - 1
    );

    retry_count_ = 0;

    xEventGroupClearBits(
        static_cast<EventGroupHandle_t>(event_group_),
        WIFI_CONNECTED_BIT | WIFI_FAILED_BIT
    );

    esp_err_t result =
        esp_wifi_set_config(
            WIFI_IF_STA,
            &config
        );

    if (result != ESP_OK) {
        return result;
    }

    if (!wifi_started_) {
        result =
            esp_wifi_start();

        if (result == ESP_OK) {
            wifi_started_ = true;
        }

        return result;
    }

    return esp_wifi_connect();
}


bool WifiManager::wait_for_connection(
    TickType_t timeout_ticks
)
{
    if (event_group_ == nullptr) {
        return false;
    }

    const EventBits_t bits =
        xEventGroupWaitBits(
            event_group_,
            WIFI_CONNECTED_BIT | WIFI_FAILED_BIT,
            pdFALSE,
            pdFALSE,
            timeout_ticks
        );

    return (
        (bits & WIFI_CONNECTED_BIT) != 0
    );
}


bool WifiManager::is_connected() const
{
    if (event_group_ == nullptr) {
        return false;
    }

    return (
        (xEventGroupGetBits(
            static_cast<EventGroupHandle_t>(event_group_)
        ) & WIFI_CONNECTED_BIT) != 0
    );
}


esp_err_t WifiManager::disconnect()
{
    if (!wifi_started_) {
        return ESP_OK;
    }

    xEventGroupClearBits(
        static_cast<EventGroupHandle_t>(event_group_),
        WIFI_CONNECTED_BIT
    );

    esp_err_t result =
        esp_wifi_disconnect();

    esp_err_t stop_result =
        esp_wifi_stop();

    wifi_started_ = false;

    if (result != ESP_OK) {
        return result;
    }

    return stop_result;
}


void WifiManager::event_handler(
    void* arg,
    esp_event_base_t event_base,
    int32_t event_id,
    void* event_data
)
{
    auto* manager =
        static_cast<WifiManager*>(arg);

    if (
        manager == nullptr
        || manager->event_group_ == nullptr
    ) {
        return;
    }

    auto event_group =
        static_cast<EventGroupHandle_t>(
            manager->event_group_
        );

    if (
        event_base == WIFI_EVENT
        && event_id == WIFI_EVENT_STA_START
    ) {
        esp_err_t result =
            esp_wifi_connect();

        if (result != ESP_OK) {
            ESP_LOGE(
                TAG,
                "Initial Wi-Fi connection failed: %s",
                esp_err_to_name(result)
            );
        }

        return;
    }

    if (
        event_base == WIFI_EVENT
        && event_id == WIFI_EVENT_STA_DISCONNECTED
    ) {
        xEventGroupClearBits(
            event_group,
            WIFI_CONNECTED_BIT
        );

        if (
            manager->retry_count_
            < manager->max_retry_count_
        ) {
            ++manager->retry_count_;

            esp_err_t result =
                esp_wifi_connect();

            if (result != ESP_OK) {
                ESP_LOGE(
                    TAG,
                    "Wi-Fi reconnect failed: %s",
                    esp_err_to_name(result)
                );
            }

            return;
        }

        xEventGroupSetBits(
            event_group,
            WIFI_FAILED_BIT
        );

        ESP_LOGW(
            TAG,
            "Wi-Fi connection retry limit reached"
        );

        return;
    }

    if (
        event_base == IP_EVENT
        && event_id == IP_EVENT_STA_GOT_IP
        && event_data != nullptr
    ) {
        manager->retry_count_ = 0;

        xEventGroupSetBits(
            event_group,
            WIFI_CONNECTED_BIT
        );

        ESP_LOGI(
            TAG,
            "Wi-Fi connected and IP address acquired"
        );
    }
}


void WifiManager::cleanup()
{
    if (wifi_started_) {
        disconnect();
    }

    if (wifi_event_instance_ != nullptr) {
        esp_event_handler_instance_unregister(
            WIFI_EVENT,
            ESP_EVENT_ANY_ID,
            static_cast<esp_event_handler_instance_t>(
                wifi_event_instance_
            )
        );

        wifi_event_instance_ = nullptr;
    }

    if (ip_event_instance_ != nullptr) {
        esp_event_handler_instance_unregister(
            IP_EVENT,
            IP_EVENT_STA_GOT_IP,
            static_cast<esp_event_handler_instance_t>(
                ip_event_instance_
            )
        );

        ip_event_instance_ = nullptr;
    }

    if (event_group_ != nullptr) {
        vEventGroupDelete(
            static_cast<EventGroupHandle_t>(event_group_)
        );

        event_group_ = nullptr;
    }

    if (wifi_initialized_) {
        esp_wifi_deinit();
        wifi_initialized_ = false;
    }

    if (netif_ != nullptr) {
        esp_netif_destroy(
            static_cast<esp_netif_t*>(netif_)
        );

        netif_ = nullptr;
    }

    if (event_loop_created_) {
        esp_event_loop_delete_default();
        event_loop_created_ = false;
    }

    if (netif_initialized_) {
        esp_netif_deinit();
        netif_initialized_ = false;
    }

    if (nvs_initialized_) {
        nvs_flash_deinit();
        nvs_initialized_ = false;
    }

    initialized_ = false;
}


}