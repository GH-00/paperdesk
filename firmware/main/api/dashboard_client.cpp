#include "dashboard_client.hpp"

#include <utility>

namespace paperdesk {

DashboardClient::DashboardClient(
    std::string base_url
)
    : base_url_(std::move(base_url))
{
}

bool DashboardClient::fetch(
    Dashboard& dashboard
)
{
    (void)dashboard;

    /*
     * 구현 예정:
     *
     * GET {base_url}/api/v1/dashboard
     *
     * HTTP response
     *      ↓
     * JSON
     *      ↓
     * Dashboard struct
     */

    return false;
}

}
