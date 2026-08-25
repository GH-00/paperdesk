#include "paperdesk_app.hpp"

#include <utility>

#include "freertos/FreeRTOS.h"

#include "esp_log.h"


namespace {


constexpr const char* TAG =
    "PaperdeskApp";

constexpr TickType_t WIFI_WAIT_TICKS =
    pdMS_TO_TICKS(15000);


}


namespace paperdesk {


PaperdeskApp::PaperdeskApp(
    std::string dashboard_base_url
)
    : dashboard_client_(
        std::move(dashboard_base_url)
    )
{
}


bool PaperdeskApp::run(
    const char* ssid,
    const char* password
)
{
    data_available_ = false;

    const bool cache_ready =
        cache_.initialize();

    const esp_err_t wifi_result =
        wifi_manager_.initialize();

    if (
        wifi_result == ESP_OK
        && ssid != nullptr
        && password != nullptr
        && ssid[0] != '\0'
    ) {
        const esp_err_t connect_result =
            wifi_manager_.connect(
                ssid,
                password
            );

        if (
            connect_result == ESP_OK
            && wifi_manager_.wait_for_connection(
                WIFI_WAIT_TICKS
            )
        ) {
            std::string raw_json;

            if (
                dashboard_client_.fetch(
                    dashboard_,
                    &raw_json
                )
            ) {
                data_available_ = true;

                if (
                    cache_ready
                    && !cache_.save(raw_json)
                ) {
                    ESP_LOGW(
                        TAG,
                        "Dashboard cache save failed"
                    );
                }

                return true;
            }

            ESP_LOGW(
                TAG,
                "Dashboard request failed; trying cache"
            );
        } else {
            ESP_LOGW(
                TAG,
                "Wi-Fi connection failed; trying cache"
            );
        }
    } else {
        ESP_LOGW(
            TAG,
            "Wi-Fi credentials unavailable; trying cache"
        );
    }

    if (cache_ready && load_cache()) {
        return true;
    }

    ESP_LOGW(
        TAG,
        "No dashboard data available"
    );

    return false;
}


bool PaperdeskApp::data_available() const
{
    return data_available_;
}


const Dashboard& PaperdeskApp::dashboard() const
{
    return dashboard_;
}


bool PaperdeskApp::load_cache()
{
    Dashboard cached_dashboard;

    if (!cache_.load(cached_dashboard)) {
        return false;
    }

    dashboard_ =
        std::move(cached_dashboard);

    data_available_ = true;
    return true;
}


}