from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from app.models.dashboard import CalendarEvent
from app.providers.base import CalendarProvider


class MockCalendarProvider(CalendarProvider):
    def __init__(self, timezone: str):
        self.timezone = ZoneInfo(timezone)

    def get_events(
        self,
        start: datetime,
        end: datetime,
    ) -> list[CalendarEvent]:
        now = datetime.now(self.timezone)

        events = [
            CalendarEvent(
                id="event-001",
                title="Team Meeting",
                start=now.replace(
                    hour=10,
                    minute=0,
                    second=0,
                    microsecond=0,
                ),
                end=now.replace(
                    hour=11,
                    minute=0,
                    second=0,
                    microsecond=0,
                ),
                all_day=False,
            ),
            CalendarEvent(
                id="event-002",
                title="English Class",
                start=now.replace(
                    hour=19,
                    minute=30,
                    second=0,
                    microsecond=0,
                ),
                end=now.replace(
                    hour=20,
                    minute=30,
                    second=0,
                    microsecond=0,
                ),
                all_day=False,
            ),
            CalendarEvent(
                id="event-003",
                title="Project Review",
                start=(
                    now + timedelta(days=2)
                ).replace(
                    hour=14,
                    minute=0,
                    second=0,
                    microsecond=0,
                ),
                end=(
                    now + timedelta(days=2)
                ).replace(
                    hour=15,
                    minute=0,
                    second=0,
                    microsecond=0,
                ),
                all_day=False,
            ),
        ]

        return [
            event
            for event in events
            if start <= event.start < end
        ]
