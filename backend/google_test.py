from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from app.providers.google_calendar import GoogleCalendarProvider


def main():
    timezone = ZoneInfo(
        "Asia/Seoul"
    )

    now = datetime.now(
        timezone
    )

    provider = (
        GoogleCalendarProvider(
            timezone="Asia/Seoul"
        )
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

    print(
        f"Fetched {len(events)} events"
    )

    for event in events[:20]:
        print(
            event.start,
            "|",
            event.title,
            "| all_day=",
            event.all_day,
        )


if __name__ == "__main__":
    main()
