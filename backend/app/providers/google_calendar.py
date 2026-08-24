from datetime import date, datetime, time
from pathlib import Path
from zoneinfo import ZoneInfo

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from app.models.dashboard import CalendarEvent
from app.providers.base import CalendarProvider


SCOPES = [
    "https://www.googleapis.com/auth/calendar.readonly"
]

BACKEND_DIR = Path(__file__).resolve().parents[2]

SECRETS_DIR = BACKEND_DIR / "secrets"

CREDENTIALS_FILE = (
    SECRETS_DIR
    / "credentials.json"
)

TOKEN_FILE = (
    SECRETS_DIR
    / "token.json"
)


class GoogleCalendarProvider(CalendarProvider):
    def __init__(
        self,
        timezone: str,
    ):
        self.timezone = ZoneInfo(
            timezone
        )

    def _get_credentials(
        self,
    ) -> Credentials:
        credentials = None

        if TOKEN_FILE.exists():
            credentials = (
                Credentials
                .from_authorized_user_file(
                    TOKEN_FILE,
                    SCOPES,
                )
            )

        if (
            credentials
            and credentials.expired
            and credentials.refresh_token
        ):
            credentials.refresh(
                Request()
            )

        elif (
            not credentials
            or not credentials.valid
        ):
            if not CREDENTIALS_FILE.exists():
                raise FileNotFoundError(
                    "Google OAuth credentials not found: "
                    f"{CREDENTIALS_FILE}"
                )

            flow = (
                InstalledAppFlow
                .from_client_secrets_file(
                    CREDENTIALS_FILE,
                    SCOPES,
                )
            )

            credentials = (
                flow.run_local_server(
                    port=0
                )
            )

        SECRETS_DIR.mkdir(
            parents=True,
            exist_ok=True,
        )

        TOKEN_FILE.write_text(
            credentials.to_json(),
            encoding="utf-8",
        )

        return credentials

    def _parse_event_datetime(
        self,
        value: dict,
    ) -> tuple[
        datetime,
        bool,
    ]:
        if "dateTime" in value:
            event_datetime = (
                datetime.fromisoformat(
                    value["dateTime"]
                    .replace(
                        "Z",
                        "+00:00",
                    )
                )
            )

            return (
                event_datetime
                .astimezone(
                    self.timezone
                ),
                False,
            )

        event_date = (
            date.fromisoformat(
                value["date"]
            )
        )

        event_datetime = datetime.combine(
            event_date,
            time.min,
            tzinfo=self.timezone,
        )

        return (
            event_datetime,
            True,
        )

    def get_events(
        self,
        start: datetime,
        end: datetime,
    ) -> list[CalendarEvent]:
        credentials = (
            self._get_credentials()
        )

        service = build(
            "calendar",
            "v3",
            credentials=credentials,
            cache_discovery=False,
        )

        result = (
            service.events()
            .list(
                calendarId="primary",
                timeMin=start.isoformat(),
                timeMax=end.isoformat(),
                singleEvents=True,
                orderBy="startTime",
                maxResults=250,
                timeZone=str(
                    self.timezone
                ),
            )
            .execute()
        )

        items = result.get(
            "items",
            [],
        )

        events = []

        for item in items:
            start_datetime, all_day = (
                self._parse_event_datetime(
                    item["start"]
                )
            )

            end_datetime, _ = (
                self._parse_event_datetime(
                    item["end"]
                )
            )

            events.append(
                CalendarEvent(
                    id=item.get(
                        "id",
                        "",
                    ),
                    title=item.get(
                        "summary",
                        "(No title)",
                    ),
                    start=start_datetime,
                    end=end_datetime,
                    all_day=all_day,
                )
            )

        return events
