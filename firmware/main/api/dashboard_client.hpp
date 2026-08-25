#pragma once

#include <string>

#include "../models/dashboard.hpp"


namespace paperdesk {


class DashboardClient {
public:
    explicit DashboardClient(
        std::string base_url
    );

    bool fetch(
        Dashboard& dashboard,
        std::string* raw_json = nullptr
    );

private:
    std::string base_url_;
};


}
