import pytest

from app.config import settings
from app.providers.factory import get_calendar_provider


@pytest.fixture(autouse=True)
def force_test_configuration(monkeypatch):
    """
    Tests must never call the real Google Calendar API.

    The application may use:
        CALENDAR_PROVIDER=google

    but pytest always overrides it with:
        CALENDAR_PROVIDER=mock
    """

    monkeypatch.setattr(
        settings,
        "calendar_provider",
        "mock",
    )

    monkeypatch.setattr(
        settings,
        "device_name",
        "paperdesk-test",
    )

    # Provider factory uses lru_cache,
    # so clear any provider created before the test.
    get_calendar_provider.cache_clear()

    yield

    get_calendar_provider.cache_clear()
