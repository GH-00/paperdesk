from datetime import datetime

from simulator.config import WIDTH
from simulator.common.drawing import (
    new_canvas,
    render_header,
    text_width,
    truncate_text,
)
from simulator.common.fonts import (
    FONT_FOOTER_SMALL,
    FONT_SCHEDULE_DATE,
    FONT_SCHEDULE_TIME,
    FONT_SCHEDULE_TITLE,
    FONT_SECTION,
)


def render(data):
    image, draw = new_canvas()

    generated_at = (
        datetime.fromisoformat(
            data["generated_at"]
        )
    )

    render_header(
        draw,
        "SCHEDULE",
        generated_at,
    )

    events = []

    for event in data["events"]:
        start = datetime.fromisoformat(
            event["start"]
        )

        if (
            start.date()
            >= generated_at.date()
        ):
            events.append(
                (
                    start,
                    event,
                )
            )

    events.sort(
        key=lambda item: item[0]
    )

    if not events:
        draw.text(
            (
                20,
                70,
            ),
            "No upcoming events",
            font=FONT_SECTION,
            fill=0,
        )

        return image

    current_y = 52
    previous_date = None

    for start, event in events:
        event_date = (
            start.date()
        )

        if current_y > 235:
            break

        if (
            event_date
            != previous_date
        ):
            if (
                event_date
                == generated_at.date()
            ):
                date_label = "TODAY"

            else:
                date_label = (
                    start.strftime(
                        "%a · %b %d"
                    ).upper()
                )

            draw.text(
                (
                    14,
                    current_y,
                ),
                date_label,
                font=FONT_SCHEDULE_DATE,
                fill=0,
            )

            draw.line(
                (
                    14,
                    current_y + 20,
                    WIDTH - 14,
                    current_y + 20,
                ),
                fill=0,
                width=1,
            )

            current_y += 30

            previous_date = (
                event_date
            )

        if event.get(
            "all_day",
            False,
        ):
            time_text = "ALL DAY"

        else:
            time_text = (
                start.strftime(
                    "%H:%M"
                )
            )

        draw.text(
            (
                18,
                current_y,
            ),
            time_text,
            font=FONT_SCHEDULE_TIME,
            fill=0,
        )

        title = truncate_text(
            draw,
            event["title"],
            FONT_SCHEDULE_TITLE,
            285,
        )

        draw.text(
            (
                88,
                current_y - 1,
            ),
            title,
            font=FONT_SCHEDULE_TITLE,
            fill=0,
        )

        current_y += 27

    footer_y = 266

    draw.line(
        (
            0,
            footer_y,
            WIDTH,
            footer_y,
        ),
        fill=0,
        width=1,
    )

    event_count_text = (
        f"{len(events)} UPCOMING"
    )

    draw.text(
        (
            12,
            footer_y + 10,
        ),
        event_count_text,
        font=FONT_FOOTER_SMALL,
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

    draw.text(
        (
            WIDTH
            - sync_width
            - 12,
            footer_y + 10,
        ),
        sync_text,
        font=FONT_FOOTER_SMALL,
        fill=0,
    )

    return image
