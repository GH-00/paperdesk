from pathlib import Path

from PIL import ImageFont


def load_font(size: int):
    candidates = [
        "C:/Windows/Fonts/malgun.ttf",
        "C:/Windows/Fonts/segoeui.ttf",
        "C:/Windows/Fonts/arial.ttf",
    ]

    for path in candidates:
        if Path(path).exists():
            return ImageFont.truetype(
                path,
                size,
            )

    return ImageFont.load_default()


FONT_HEADER = load_font(19)

FONT_WEEKDAY = load_font(9)
FONT_DAY = load_font(10)

FONT_SECTION = load_font(13)
FONT_EVENT = load_font(10)

FONT_SCHEDULE_DATE = load_font(12)
FONT_SCHEDULE_TIME = load_font(9)
FONT_SCHEDULE_TITLE = load_font(11)

FONT_FOOTER_MAIN = load_font(12)
FONT_FOOTER_SMALL = load_font(8)

FONT_HOME_LABEL = load_font(11)
FONT_HOME_VALUE_LARGE = load_font(30)
FONT_HOME_VALUE_MEDIUM = load_font(21)
FONT_HOME_SMALL = load_font(8)
