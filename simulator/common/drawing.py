from PIL import Image, ImageDraw

from simulator.config import HEIGHT, WIDTH
from simulator.common.fonts import FONT_HEADER


def new_canvas():
    image = Image.new(
        "1",
        (
            WIDTH,
            HEIGHT,
        ),
        1,
    )

    draw = ImageDraw.Draw(image)

    return image, draw


def text_width(draw, text, font):
    bbox = draw.textbbox(
        (0, 0),
        text,
        font=font,
    )

    return bbox[2] - bbox[0]


def text_height(draw, text, font):
    bbox = draw.textbbox(
        (0, 0),
        text,
        font=font,
    )

    return bbox[3] - bbox[1]


def truncate_text(
    draw,
    text,
    font,
    max_width,
):
    if (
        text_width(
            draw,
            text,
            font,
        )
        <= max_width
    ):
        return text

    suffix = "..."

    while text:
        candidate = text + suffix

        if (
            text_width(
                draw,
                candidate,
                font,
            )
            <= max_width
        ):
            return candidate

        text = text[:-1]

    return suffix


def draw_centered(
    draw,
    text,
    font,
    center_x,
    y,
    fill=0,
):
    width = text_width(
        draw,
        text,
        font,
    )

    draw.text(
        (
            center_x - width / 2,
            y,
        ),
        text,
        font=font,
        fill=fill,
    )


def render_header(
    draw,
    title,
    generated_at,
):
    draw.text(
        (
            12,
            8,
        ),
        title,
        font=FONT_HEADER,
        fill=0,
    )

    current_time = generated_at.strftime(
        "%H:%M"
    )

    current_time_width = text_width(
        draw,
        current_time,
        FONT_HEADER,
    )

    draw.text(
        (
            WIDTH
            - current_time_width
            - 12,
            8,
        ),
        current_time,
        font=FONT_HEADER,
        fill=0,
    )

    draw.line(
        (
            0,
            38,
            WIDTH,
            38,
        ),
        fill=0,
        width=1,
    )
