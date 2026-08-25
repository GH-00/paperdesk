#include "dashboard_cache.hpp"

#include <cstdio>
#include <fstream>
#include <iterator>
#include <utility>

#include "../api/dashboard_parser.hpp"

#include "esp_err.h"
#include "esp_log.h"
#include "esp_spiffs.h"


namespace {


constexpr const char* TAG =
    "DashboardCache";

constexpr const char* CACHE_PATH =
    "/spiffs/dashboard.json";

constexpr const char* TEMP_PATH =
    "/spiffs/dashboard.json.tmp";

constexpr const char* PARTITION_LABEL =
    "storage";


}


namespace paperdesk {


DashboardCache::~DashboardCache()
{
    if (initialized_) {
        esp_vfs_spiffs_unregister(
            PARTITION_LABEL
        );
    }
}


bool DashboardCache::initialize()
{
    if (initialized_) {
        return true;
    }

    esp_vfs_spiffs_conf_t config = {};

    config.base_path = "/spiffs";
    config.partition_label = PARTITION_LABEL;
    config.max_files = 2;
    config.format_if_mount_failed = false;

    const esp_err_t result =
        esp_vfs_spiffs_register(
            &config
        );

    if (result != ESP_OK) {
        ESP_LOGW(
            TAG,
            "Cache filesystem unavailable: %s",
            esp_err_to_name(result)
        );

        return false;
    }

    initialized_ = true;
    return true;
}


bool DashboardCache::save(
    const std::string& json
)
{
    if (
        !initialized_
        || json.empty()
    ) {
        return false;
    }

    Dashboard validated_dashboard;

    if (
        !DashboardParser::parse(
            json,
            validated_dashboard
        )
    ) {
        return false;
    }

    std::ofstream temporary_file(
        TEMP_PATH,
        std::ios::binary
        | std::ios::trunc
    );

    if (!temporary_file.is_open()) {
        return false;
    }

    temporary_file.write(
        json.data(),
        static_cast<std::streamsize>(
            json.size()
        )
    );

    temporary_file.flush();

    if (!temporary_file.good()) {
        temporary_file.close();
        std::remove(TEMP_PATH);
        return false;
    }

    temporary_file.close();

    if (
        std::rename(
            TEMP_PATH,
            CACHE_PATH
        ) != 0
    ) {
        std::remove(TEMP_PATH);
        return false;
    }

    return true;
}


bool DashboardCache::load(
    Dashboard& dashboard
)
{
    if (!initialized_) {
        return false;
    }

    std::ifstream cache_file(
        CACHE_PATH,
        std::ios::binary
    );

    if (!cache_file.is_open()) {
        return false;
    }

    const std::string json(
        (
            std::istreambuf_iterator<char>(
                cache_file
            )
        ),
        std::istreambuf_iterator<char>()
    );

    if (!cache_file.good() && !cache_file.eof()) {
        return false;
    }

    Dashboard parsed_dashboard;

    if (
        !DashboardParser::parse(
            json,
            parsed_dashboard
        )
    ) {
        return false;
    }

    dashboard =
        std::move(parsed_dashboard);

    return true;
}


bool DashboardCache::exists() const
{
    if (!initialized_) {
        return false;
    }

    std::ifstream cache_file(
        CACHE_PATH,
        std::ios::binary
    );

    return cache_file.good();
}


bool DashboardCache::clear()
{
    if (!initialized_) {
        return false;
    }

    return (
        std::remove(CACHE_PATH) == 0
        || !exists()
    );
}


}
