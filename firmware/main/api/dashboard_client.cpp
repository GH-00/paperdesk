#include "dashboard_client.hpp"

#include <cstddef>
#include <string>
#include <utility>

#include "dashboard_parser.hpp"

#include "esp_err.h"
#include "esp_http_client.h"
#include "esp_log.h"


namespace {


constexpr const char* TAG =
    "DashboardClient";

constexpr int HTTP_TIMEOUT_MS =
    5000;

constexpr std::size_t MAX_RESPONSE_BYTES =
    64 * 1024;


struct HttpResponseBuffer {
    std::string body;
    bool overflow = false;
};


std::string build_dashboard_url(
    const std::string& base_url
)
{
    if (
        !base_url.empty()
        && base_url.back() == '/'
    ) {
        return (
            base_url
            + "api/v1/dashboard"
        );
    }

    return (
        base_url
        + "/api/v1/dashboard"
    );
}


esp_err_t http_event_handler(
    esp_http_client_event_t* event
)
{
    if (
        event == nullptr
        || event->user_data == nullptr
    ) {
        return ESP_OK;
    }

    auto* response =
        static_cast<HttpResponseBuffer*>(
            event->user_data
        );

    switch (event->event_id) {
        case HTTP_EVENT_ON_DATA: {
            if (
                event->data == nullptr
                || event->data_len <= 0
            ) {
                break;
            }

            const auto incoming_size =
                static_cast<std::size_t>(
                    event->data_len
                );

            if (
                response->body.size()
                + incoming_size
                > MAX_RESPONSE_BYTES
            ) {
                response->overflow = true;

                ESP_LOGE(
                    TAG,
                    "HTTP response exceeded %u bytes",
                    static_cast<unsigned int>(
                        MAX_RESPONSE_BYTES
                    )
                );

                return ESP_FAIL;
            }

            response->body.append(
                static_cast<const char*>(
                    event->data
                ),
                incoming_size
            );

            break;
        }

        default:
            break;
    }

    return ESP_OK;
}


}


namespace paperdesk {


DashboardClient::DashboardClient(
    std::string base_url
)
    : base_url_(
        std::move(base_url)
    )
{
}


bool DashboardClient::fetch(
    Dashboard& dashboard,
    std::string* raw_json
)
{
    const std::string url =
        build_dashboard_url(
            base_url_
        );

    HttpResponseBuffer response;

    esp_http_client_config_t config = {};

    config.url =
        url.c_str();

    config.timeout_ms =
        HTTP_TIMEOUT_MS;

    config.event_handler =
        http_event_handler;

    config.user_data =
        &response;

    config.user_agent =
        "paperdesk-firmware/0.1";

    ESP_LOGI(
        TAG,
        "GET %s",
        url.c_str()
    );

    esp_http_client_handle_t client =
        esp_http_client_init(
            &config
        );

    if (client == nullptr) {
        ESP_LOGE(
            TAG,
            "Failed to initialize HTTP client"
        );

        return false;
    }

    esp_err_t result =
        esp_http_client_set_method(
            client,
            HTTP_METHOD_GET
        );

    if (result != ESP_OK) {
        ESP_LOGE(
            TAG,
            "Failed to configure GET method: %s",
            esp_err_to_name(result)
        );

        esp_http_client_cleanup(
            client
        );

        return false;
    }

    result =
        esp_http_client_set_header(
            client,
            "Accept",
            "application/json"
        );

    if (result != ESP_OK) {
        ESP_LOGE(
            TAG,
            "Failed to set Accept header: %s",
            esp_err_to_name(result)
        );

        esp_http_client_cleanup(
            client
        );

        return false;
    }

    result =
        esp_http_client_perform(
            client
        );

    if (result != ESP_OK) {
        ESP_LOGE(
            TAG,
            "HTTP request failed: %s",
            esp_err_to_name(result)
        );

        esp_http_client_cleanup(
            client
        );

        return false;
    }

    const int status_code =
        esp_http_client_get_status_code(
            client
        );

    ESP_LOGI(
        TAG,
        "HTTP status=%d, response=%u bytes",
        status_code,
        static_cast<unsigned int>(
            response.body.size()
        )
    );

    esp_http_client_cleanup(
        client
    );

    if (response.overflow) {
        ESP_LOGE(
            TAG,
            "Dashboard response too large"
        );

        return false;
    }

    if (status_code != 200) {
        ESP_LOGE(
            TAG,
            "Unexpected HTTP status: %d",
            status_code
        );

        return false;
    }

    if (response.body.empty()) {
        ESP_LOGE(
            TAG,
            "Dashboard response body is empty"
        );

        return false;
    }

    if (
        !DashboardParser::parse(
            response.body,
            dashboard
        )
    ) {
        ESP_LOGE(
            TAG,
            "Failed to parse dashboard JSON"
        );

        return false;
    }

    if (raw_json != nullptr) {
        *raw_json = response.body;
    }

    ESP_LOGI(
        TAG,
        "Dashboard fetched successfully"
    );

    return true;
}


}
