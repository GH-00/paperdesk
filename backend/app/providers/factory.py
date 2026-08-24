from functools import lru_cache

from app.config import settings
from app.providers.base import CalendarProvider
from app.providers.google_calendar import GoogleCalendarProvider
from app.providers.mock_calendar import MockCalendarProvider


@lru_cache
def get_calendar_provider() -> CalendarProvider:
    if settings.calendar_provider == "mock":
        return MockCalendarProvider(
            timezone=settings.timezone,
        )

    if settings.calendar_provider == "google":
        return GoogleCalendarProvider(
            timezone=settings.timezone,
        )

    raise ValueError(
        f"Unsupported calendar provider: "
        f"{settings.calendar_provider}"
    )
