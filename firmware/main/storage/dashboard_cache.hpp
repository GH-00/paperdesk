#pragma once

#include <string>

#include "../models/dashboard.hpp"

namespace paperdesk {

class DashboardCache {
public:
    ~DashboardCache();

    DashboardCache(const DashboardCache&) = delete;
    DashboardCache& operator=(const DashboardCache&) = delete;

    bool initialize();

    bool save(
        const std::string& json
    );

    bool load(
        Dashboard& dashboard
    );

    bool exists() const;

    bool clear();

private:
    bool initialized_ = false;
};

}
