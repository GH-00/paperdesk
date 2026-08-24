#include "models/dashboard.hpp"
#include "pages/page.hpp"

extern "C" void app_main()
{
    paperdesk::Dashboard dashboard;

    paperdesk::Page current_page =
        paperdesk::Page::Calendar;

    (void)dashboard;
    (void)current_page;
}
