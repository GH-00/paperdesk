#if __has_include("config/wifi_credentials.hpp")
#include "config/wifi_credentials.hpp"
#else
#include "config/wifi_credentials.example.hpp"
#endif

#include "application/paperdesk_app.hpp"


namespace {


constexpr const char* DASHBOARD_BASE_URL =
#ifdef CONFIG_PAPERDESK_DASHBOARD_BASE_URL
    CONFIG_PAPERDESK_DASHBOARD_BASE_URL;
#else
    "";
#endif


}

extern "C" void app_main()
{
    static paperdesk::PaperdeskApp app(
        DASHBOARD_BASE_URL
    );

    const bool data_available =
        app.run(
            paperdesk::wifi_credentials::SSID,
            paperdesk::wifi_credentials::PASSWORD
        );

    (void)data_available;
}
