from datetime import datetime

from simulator.config import WIDTH
from simulator.common.drawing import (
    draw_centered,
    new_canvas,
    render_header,
    text_width,
    truncate_text,
)
from simulator.common.fonts import (
    FONT_FOOTER_SMALL,
    FONT_HOME_LABEL,
    FONT_HOME_SMALL,
    FONT_HOME_VALUE_LARGE,
    FONT_HOME_VALUE_MEDIUM,
)


def render(data):
    image, draw = new_canvas()

    generated_at = (
        datetime.fromisoformat(
            data["generated_at"]
        )
    )

    environment = (
        data["environment"]
    )

    ddays = data["ddays"]

    render_header(
        draw,
        "HOME",
        generated_at,
    )

    split_x = 244
    footer_y = 268

    # Main vertical separator
    draw.line(
        (
            split_x,
            38,
            split_x,
            footer_y,
        ),
        fill=0,
        width=1,
    )

    # ========================================================
    # Indoor
    # ========================================================

    draw.text(
        (
            14,
            53,
        ),
        "INDOOR",
        font=FONT_HOME_LABEL,
        fill=0,
    )

    draw.line(
        (
            14,
            73,
            228,
            73,
        ),
        fill=0,
        width=1,
    )

    left_center_x = (
        split_x / 2
    )

    temperature_text = (
        f'{environment["temperature"]:.1f} C'
    )

    draw_centered(
        draw,
        temperature_text,
        FONT_HOME_VALUE_LARGE,
        left_center_x,
        92,
    )

    draw_centered(
        draw,
        "TEMPERATURE",
        FONT_HOME_SMALL,
        left_center_x,
        138,
    )

    humidity_text = (
        f'{environment["humidity"]:.0f}%'
    )

    draw_centered(
        draw,
        humidity_text,
        FONT_HOME_VALUE_MEDIUM,
        left_center_x,
        169,
    )

    draw_centered(
        draw,
        "HUMIDITY",
        FONT_HOME_SMALL,
        left_center_x,
        203,
    )

    source_text = (
        "SOURCE · "
        + environment[
            "source"
        ].upper()
    )

    draw_centered(
        draw,
        source_text,
        FONT_HOME_SMALL,
        left_center_x,
        239,
    )

    # ========================================================
    # D-Day
    # ========================================================

    right_x = 258

    right_center_x = (
        split_x
        + (
            WIDTH
            - split_x
        ) / 2
    )

    draw.text(
        (
            right_x,
            53,
        ),
        "D-DAY",
        font=FONT_HOME_LABEL,
        fill=0,
    )

    draw.line(
        (
            right_x,
            73,
            WIDTH - 14,
            73,
        ),
        fill=0,
        width=1,
    )

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

        draw_centered(
            draw,
            dday_value,
            FONT_HOME_VALUE_MEDIUM,
            right_center_x,
            88,
        )

        dday_title = (
            truncate_text(
                draw,
                dday["title"],
                FONT_HOME_SMALL,
                120,
            )
        )

        draw_centered(
            draw,
            dday_title,
            FONT_HOME_SMALL,
            right_center_x,
            125,
        )

    # ========================================================
    # Device
    # ========================================================

    draw.line(
        (
            split_x,
            153,
            WIDTH,
            153,
        ),
        fill=0,
        width=1,
    )

    draw.text(
        (
            right_x,
            167,
        ),
        "DEVICE",
        font=FONT_HOME_LABEL,
        fill=0,
    )

    draw.line(
        (
            right_x,
            187,
            WIDTH - 14,
            187,
        ),
        fill=0,
        width=1,
    )

    rows = [
        (
            "API",
            "LOCAL",
        ),
        (
            "DATA",
            environment[
                "source"
            ].upper(),
        ),
        (
            "SYNC",
            generated_at.strftime(
                "%H:%M"
            ),
        ),
    ]

    row_y = 198

    for label, value in rows:
        draw.text(
            (
                right_x,
                row_y,
            ),
            label,
            font=FONT_HOME_SMALL,
            fill=0,
        )

        value_width = (
            text_width(
                draw,
                value,
                FONT_HOME_SMALL,
            )
        )

        draw.text(
            (
                WIDTH
                - 14
                - value_width,
                row_y,
            ),
            value,
            font=FONT_HOME_SMALL,
            fill=0,
        )

        row_y += 20

    # ========================================================
    # Footer
    # ========================================================

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

    date_text = (
        generated_at.strftime(
            "%a · %b %d · %Y"
        ).upper()
    )

    draw.text(
        (
            12,
            footer_y + 10,
        ),
        date_text,
        font=FONT_FOOTER_SMALL,
        fill=0,
    )

    return image
