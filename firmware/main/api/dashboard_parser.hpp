#pragma once

#include <string>

#include "../models/dashboard.hpp"

namespace paperdesk {

class DashboardParser {
public:
    static bool parse(
        const std::string& json,
        Dashboard& dashboard
    );
};

}
