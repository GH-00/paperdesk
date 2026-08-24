#pragma once

namespace paperdesk {

enum class Page {
    Calendar = 0,
    Schedule,
    Home,
};

inline Page next_page(Page current)
{
    switch (current) {
        case Page::Calendar:
            return Page::Schedule;

        case Page::Schedule:
            return Page::Home;

        case Page::Home:
        default:
            return Page::Calendar;
    }
}

}
