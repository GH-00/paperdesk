#include "dashboard_parser.hpp"

#include <utility>

#include "cJSON.h"

namespace {

bool get_required_string(
    const cJSON* object,
    const char* key,
    std::string& output
)
{
    const cJSON* item =
        cJSON_GetObjectItemCaseSensitive(object, key);

    if (
        item == nullptr ||
        !cJSON_IsString(item) ||
        item->valuestring == nullptr
    ) {
        return false;
    }

    output = item->valuestring;
    return true;
}


bool get_required_int(
    const cJSON* object,
    const char* key,
    int& output
)
{
    const cJSON* item =
        cJSON_GetObjectItemCaseSensitive(object, key);

    if (
        item == nullptr ||
        !cJSON_IsNumber(item)
    ) {
        return false;
    }

    output = item->valueint;
    return true;
}


bool get_required_float(
    const cJSON* object,
    const char* key,
    float& output
)
{
    const cJSON* item =
        cJSON_GetObjectItemCaseSensitive(object, key);

    if (
        item == nullptr ||
        !cJSON_IsNumber(item)
    ) {
        return false;
    }

    output =
        static_cast<float>(item->valuedouble);

    return true;
}


bool get_required_bool(
    const cJSON* object,
    const char* key,
    bool& output
)
{
    const cJSON* item =
        cJSON_GetObjectItemCaseSensitive(object, key);

    if (
        item == nullptr ||
        !cJSON_IsBool(item)
    ) {
        return false;
    }

    output = cJSON_IsTrue(item);
    return true;
}


bool parse_device(
    const cJSON* root,
    paperdesk::DeviceInfo& device
)
{
    const cJSON* object =
        cJSON_GetObjectItemCaseSensitive(
            root,
            "device"
        );

    if (
        object == nullptr ||
        !cJSON_IsObject(object)
    ) {
        return false;
    }

    return
        get_required_string(
            object,
            "name",
            device.name
        ) &&
        get_required_string(
            object,
            "timezone",
            device.timezone
        );
}


bool parse_calendar(
    const cJSON* root,
    paperdesk::CalendarInfo& calendar
)
{
    const cJSON* object =
        cJSON_GetObjectItemCaseSensitive(
            root,
            "calendar"
        );

    if (
        object == nullptr ||
        !cJSON_IsObject(object)
    ) {
        return false;
    }

    return
        get_required_int(
            object,
            "year",
            calendar.year
        ) &&
        get_required_int(
            object,
            "month",
            calendar.month
        ) &&
        get_required_int(
            object,
            "today",
            calendar.today
        );
}


bool parse_events(
    const cJSON* root,
    std::vector<paperdesk::CalendarEvent>& events
)
{
    const cJSON* array =
        cJSON_GetObjectItemCaseSensitive(
            root,
            "events"
        );

    if (
        array == nullptr ||
        !cJSON_IsArray(array)
    ) {
        return false;
    }

    events.clear();

    const cJSON* item = nullptr;

    cJSON_ArrayForEach(item, array) {
        if (!cJSON_IsObject(item)) {
            return false;
        }

        paperdesk::CalendarEvent event;

        if (
            !get_required_string(
                item,
                "id",
                event.id
            ) ||
            !get_required_string(
                item,
                "title",
                event.title
            ) ||
            !get_required_string(
                item,
                "start",
                event.start
            ) ||
            !get_required_string(
                item,
                "end",
                event.end
            ) ||
            !get_required_bool(
                item,
                "all_day",
                event.all_day
            )
        ) {
            return false;
        }

        events.push_back(
            std::move(event)
        );
    }

    return true;
}


bool parse_ddays(
    const cJSON* root,
    std::vector<paperdesk::DDay>& ddays
)
{
    const cJSON* array =
        cJSON_GetObjectItemCaseSensitive(
            root,
            "ddays"
        );

    if (
        array == nullptr ||
        !cJSON_IsArray(array)
    ) {
        return false;
    }

    ddays.clear();

    const cJSON* item = nullptr;

    cJSON_ArrayForEach(item, array) {
        if (!cJSON_IsObject(item)) {
            return false;
        }

        paperdesk::DDay dday;

        if (
            !get_required_string(
                item,
                "title",
                dday.title
            ) ||
            !get_required_string(
                item,
                "date",
                dday.date
            ) ||
            !get_required_int(
                item,
                "days_remaining",
                dday.days_remaining
            )
        ) {
            return false;
        }

        ddays.push_back(
            std::move(dday)
        );
    }

    return true;
}


bool parse_environment(
    const cJSON* root,
    paperdesk::Environment& environment
)
{
    const cJSON* object =
        cJSON_GetObjectItemCaseSensitive(
            root,
            "environment"
        );

    if (
        object == nullptr ||
        !cJSON_IsObject(object)
    ) {
        return false;
    }

    return
        get_required_float(
            object,
            "temperature",
            environment.temperature
        ) &&
        get_required_float(
            object,
            "humidity",
            environment.humidity
        ) &&
        get_required_string(
            object,
            "source",
            environment.source
        );
}

}


namespace paperdesk {

bool DashboardParser::parse(
    const std::string& json,
    Dashboard& dashboard
)
{
    cJSON* root =
        cJSON_Parse(json.c_str());

    if (root == nullptr) {
        return false;
    }

    if (!cJSON_IsObject(root)) {
        cJSON_Delete(root);
        return false;
    }

    Dashboard parsed;

    const bool success =
        get_required_string(
            root,
            "generated_at",
            parsed.generated_at
        ) &&
        parse_device(
            root,
            parsed.device
        ) &&
        parse_calendar(
            root,
            parsed.calendar
        ) &&
        parse_events(
            root,
            parsed.events
        ) &&
        parse_ddays(
            root,
            parsed.ddays
        ) &&
        parse_environment(
            root,
            parsed.environment
        );

    cJSON_Delete(root);

    if (!success) {
        return false;
    }

    dashboard = std::move(parsed);

    return true;
}

}
