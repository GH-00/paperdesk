#pragma once

#include <string>

#include "../api/dashboard_client.hpp"
#include "../models/dashboard.hpp"
#include "../network/wifi_manager.hpp"
#include "../storage/dashboard_cache.hpp"

namespace paperdesk {

class PaperdeskApp {
public:
    explicit PaperdeskApp(
        std::string dashboard_base_url
    );

    bool run(
        const char* ssid,
        const char* password
    );

    bool data_available() const;

    const Dashboard& dashboard() const;

private:
    bool load_cache();

    Dashboard dashboard_;
    DashboardCache cache_;
    WifiManager wifi_manager_;
    DashboardClient dashboard_client_;
    bool data_available_ = false;
};

}