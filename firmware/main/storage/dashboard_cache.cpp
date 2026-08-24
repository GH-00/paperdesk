#include "dashboard_cache.hpp"

namespace paperdesk {

bool DashboardCache::save(
    const Dashboard& dashboard
)
{
    (void)dashboard;

    // TODO:
    // JSON or binary serialization
    // -> flash filesystem / NVS

    return false;
}

bool DashboardCache::load(
    Dashboard& dashboard
)
{
    (void)dashboard;

    return false;
}

}
