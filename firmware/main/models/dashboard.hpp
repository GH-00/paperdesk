#pragma once

#include <string>
#include <vector>

namespace paperdesk {

struct DeviceInfo {
    std::string name;
    std::string timezone;
};

struct CalendarInfo {
    int year = 0;
    int month = 0;
    int today = 0;
};

struct CalendarEvent {
    std::string id;
    std::string title;
    std::string start;
    std::string end;
    bool all_day = false;
};

struct DDay {
    std::string title;
    std::string date;
    int days_remaining = 0;
};

struct Environment {
    float temperature = 0.0F;
    float humidity = 0.0F;
    std::string source;
};

struct Dashboard {
    std::string generated_at;

    DeviceInfo device;
    CalendarInfo calendar;

    std::vector<CalendarEvent> events;
    std::vector<DDay> ddays;

    Environment environment;
};

}
