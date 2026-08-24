#pragma once

#include "../models/dashboard.hpp"

namespace paperdesk {

class DashboardCache {
public:
    bool save(
        const Dashboard& dashboard
    );

    bool load(
        Dashboard& dashboard
    );
};

}
