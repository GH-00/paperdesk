from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from app.providers.mock_calendar import MockCalendarProvider


def test_mock_calendar_provider():
    timezone = ZoneInfo(
        "Asia/Seoul"
    )

    now = datetime.now(
        timezone
    )

    provider = MockCalendarProvider(
        timezone="Asia/Seoul"
    )

    events = provider.get_events(
        start=now.replace(
            day=1,
            hour=0,
            minute=0,
            second=0,
            microsecond=0,
        ),
        end=now + timedelta(
            days=60
        ),
    )

    assert len(events) == 3

    titles = {
        event.title
        for event in events
    }

    assert titles == {
        "Team Meeting",
        "English Class",
        "Project Review",
    }

    for event in events:
        assert event.start.tzinfo is not None
        assert event.end.tzinfo is not None
