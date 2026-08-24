import calendar
from datetime import datetime

from simulator.config import WIDTH
from simulator.common.drawing import (
    new_canvas,
    render_header,
    text_height,
    text_width,
    truncate_text,
)
from simulator.common.fonts import (
    FONT_DAY,
    FONT_EVENT,
    FONT_FOOTER_MAIN,
    FONT_FOOTER_SMALL,
    FONT_SECTION,
    FONT_WEEKDAY,
)


def get_event_days(
    data,
    year,
    month,
):
    event_days = set()

    for event in data["events"]:
        start = datetime.fromisoformat(
            event["start"]
        )

        if (
            start.year == year
            and start.month == month
        ):
            event_days.add(
                start.day
            )

    return event_days


def render_calendar_grid(
    draw,
    data,
):
    cal = data["calendar"]

    year = cal["year"]
    month = cal["month"]
    today = cal["today"]

    event_days = get_event_days(
        data,
        year,
        month,
    )

    x0 = 11
    y0 = 51

    calendar_width = 228
    column_width = (
        calendar_width / 7
    )

    weekdays = [
        "S",
        "M",
        "T",
        "W",
        "T",
        "F",
        "S",
    ]

    for index, weekday in enumerate(
        weekdays
    ):
        center_x = (
            x0
            + index * column_width
            + column_width / 2
        )

        width = text_width(
            draw,
            weekday,
            FONT_WEEKDAY,
        )

        draw.text(
            (
                center_x - width / 2,
                y0,
            ),
            weekday,
            font=FONT_WEEKDAY,
            fill=0,
        )

    weeks = calendar.Calendar(
        firstweekday=6
    ).monthdayscalendar(
        year,
        month,
    )

    grid_top = 72
    available_height = 164

    row_height = (
        available_height
        / len(weeks)
    )

    for row_index, week in enumerate(
        weeks
    ):
        for (
            column_index,
            day,
        ) in enumerate(week):

            if day == 0:
                continue

            center_x = (
                x0
                + column_index
                * column_width
                + column_width / 2
            )

            center_y = (
                grid_top
                + row_index
                * row_height
                + row_height / 2
            )

            day_text = str(day)

            day_width = text_width(
                draw,
                day_text,
                FONT_DAY,
            )

            day_height = text_height(
                draw,
                day_text,
                FONT_DAY,
            )

            if day == today:
                radius = 10

                draw.ellipse(
                    (
                        center_x
                        - radius,
                        center_y
                        - radius,
                        center_x
                        + radius,
                        center_y
                        + radius,
                    ),
                    fill=0,
                )

                draw.text(
                    (
                        center_x
                        - day_width
                        / 2,
                        center_y
                        - day_height
                        / 2
                        - 2,
                    ),
                    day_text,
                    font=FONT_DAY,
                    fill=1,
                )

            else:
                draw.text(
                    (
                        center_x
                        - day_width
                        / 2,
                        center_y
                        - day_height
                        / 2
                        - 2,
                    ),
                    day_text,
                    font=FONT_DAY,
                    fill=0,
                )

            if (
                day in event_days
                and day != today
            ):
                dot_radius = 2
                dot_y = (
                    center_y + 11
                )

                draw.ellipse(
                    (
                        center_x
                        - dot_radius,
                        dot_y
                        - dot_radius,
                        center_x
                        + dot_radius,
                        dot_y
                        + dot_radius,
                    ),
                    fill=0,
                )


def render_today_events(
    draw,
    data,
):
    x0 = 263
    y0 = 51

    right_margin = 12

    draw.text(
        (
            x0,
            y0,
        ),
        "TODAY",
        font=FONT_SECTION,
        fill=0,
    )

    draw.line(
        (
            x0,
            72,
            WIDTH
            - right_margin,
            72,
        ),
        fill=0,
        width=1,
    )

    generated_at = (
        datetime.fromisoformat(
            data["generated_at"]
        )
    )

    today = (
        generated_at.date()
    )

    events = []

    for event in data["events"]:
        start = datetime.fromisoformat(
            event["start"]
        )

        if start.date() == today:
            events.append(
                (
                    start,
                    event,
                )
            )

    events.sort(
        key=lambda item: item[0]
    )

    current_y = 84

    if not events:
        draw.text(
            (
                x0,
                current_y,
            ),
            "No events",
            font=FONT_EVENT,
            fill=0,
        )

        return

    for start, event in events[:4]:
        if event.get(
            "all_day",
            False,
        ):
            time_text = "ALL"
        else:
            time_text = (
                start.strftime(
                    "%H:%M"
                )
            )

        time_width_value = (
            text_width(
                draw,
                time_text,
                FONT_EVENT,
            )
        )

        title_x = (
            x0
            + time_width_value
            + 6
        )

        available_title_width = (
            WIDTH
            - right_margin
            - title_x
        )

        title = truncate_text(
            draw,
            event["title"],
            FONT_EVENT,
            available_title_width,
        )

        draw.text(
            (
                x0,
                current_y,
            ),
            time_text,
            font=FONT_EVENT,
            fill=0,
        )

        draw.text(
            (
                title_x,
                current_y,
            ),
            title,
            font=FONT_EVENT,
            fill=0,
        )

        current_y += 30


def render_footer(
    draw,
    data,
):
    top = 246

    draw.line(
        (
            0,
            top,
            WIDTH,
            top,
        ),
        fill=0,
        width=1,
    )

    generated_at = (
        datetime.fromisoformat(
            data["generated_at"]
        )
    )

    environment = (
        data["environment"]
    )

    ddays = data["ddays"]

    if ddays:
        dday = ddays[0]

        remaining = (
            dday[
                "days_remaining"
            ]
        )

        if remaining == 0:
            dday_value = "D-DAY"

        elif remaining > 0:
            dday_value = (
                f"D-{remaining}"
            )

        else:
            dday_value = (
                f"D+"
                f"{abs(remaining)}"
            )

        title = truncate_text(
            draw,
            dday["title"],
            FONT_FOOTER_SMALL,
            68,
        )

        draw.text(
            (
                12,
                top + 13,
            ),
            title,
            font=FONT_FOOTER_SMALL,
            fill=0,
        )

        draw.text(
            (
                76,
                top + 8,
            ),
            dday_value,
            font=FONT_FOOTER_MAIN,
            fill=0,
        )

    environment_text = (
        f'{environment["temperature"]:.1f}C'
        f'  ·  '
        f'{environment["humidity"]:.0f}%'
    )

    draw.text(
        (
            195,
            top + 8,
        ),
        environment_text,
        font=FONT_FOOTER_MAIN,
        fill=0,
    )

    sync_text = (
        "SYNC "
        + generated_at.strftime(
            "%H:%M"
        )
    )

    sync_width = text_width(
        draw,
        sync_text,
        FONT_FOOTER_SMALL,
    )

    sync_x = (
        WIDTH
        - sync_width
        - 12
    )

    dot_x = sync_x - 8
    dot_y = top + 38

    draw.ellipse(
        (
            dot_x - 2,
            dot_y - 2,
            dot_x + 2,
            dot_y + 2,
        ),
        fill=0,
    )

    draw.text(
        (
            sync_x,
            top + 34,
        ),
        sync_text,
        font=FONT_FOOTER_SMALL,
        fill=0,
    )


def render(data):
    image, draw = new_canvas()

    generated_at = (
        datetime.fromisoformat(
            data["generated_at"]
        )
    )

    cal = data["calendar"]

    month_title = datetime(
        cal["year"],
        cal["month"],
        1,
    ).strftime(
        "%B %Y"
    ).upper()

    render_header(
        draw,
        month_title,
        generated_at,
    )

    draw.line(
        (
            251,
            38,
            251,
            246,
        ),
        fill=0,
        width=1,
    )

    render_calendar_grid(
        draw,
        data,
    )

    render_today_events(
        draw,
        data,
    )

    render_footer(
        draw,
        data,
    )

    return image
