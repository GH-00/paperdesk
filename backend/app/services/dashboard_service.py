from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo

from app.config import settings
from app.models.dashboard import (
    CalendarInfo,
    Dashboard,
    DDay,
    DeviceInfo,
    Environment,
)
from app.providers.factory import get_calendar_provider


def build_dashboard() -> Dashboard:
    timezone = ZoneInfo(
        settings.timezone
    )

    now = datetime.now(
        timezone
    )

    # --------------------------------------------------------
    # Calendar provider
    #
    # Start from the first day of the current month so that
    # the calendar page can also mark events that occurred
    # earlier in the month.
    # --------------------------------------------------------

    calendar_window_start = now.replace(
        day=1,
        hour=0,
        minute=0,
        second=0,
        microsecond=0,
    )

    calendar_window_end = (
        now + timedelta(days=60)
    )

    calendar_provider = (
        get_calendar_provider()
    )

    events = calendar_provider.get_events(
        start=calendar_window_start,
        end=calendar_window_end,
    )

    # --------------------------------------------------------
    # D-Day
    # --------------------------------------------------------

    if settings.dday_date:
        dday_date = date.fromisoformat(
            settings.dday_date
        )

    else:
        dday_date = (
            now.date()
            + timedelta(days=30)
        )

    dday = DDay(
        title=settings.dday_title,
        date=dday_date,
        days_remaining=(
            dday_date
            - now.date()
        ).days,
    )

    # --------------------------------------------------------
    # Dashboard
    # --------------------------------------------------------

    return Dashboard(
        generated_at=now,

        device=DeviceInfo(
            name=settings.device_name,
            timezone=settings.timezone,
        ),

        calendar=CalendarInfo(
            year=now.year,
            month=now.month,
            today=now.day,
        ),

        events=events,

        ddays=[
            dday
        ],

        environment=Environment(
            temperature=(
                settings.mock_temperature
            ),
            humidity=(
                settings.mock_humidity
            ),
            source="mock",
        ),
    )
