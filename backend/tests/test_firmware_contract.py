import json
from pathlib import Path

from app.models.dashboard import Dashboard


FIXTURE = (
    Path(__file__).resolve().parents[2]
    / "firmware"
    / "testdata"
    / "dashboard.json"
)


def test_firmware_dashboard_fixture_matches_api_model():
    with FIXTURE.open(
        "r",
        encoding="utf-8",
    ) as file:
        data = json.load(file)

    dashboard = Dashboard.model_validate(
        data
    )

    assert (
        dashboard.device.name
        == "paperdesk-dev"
    )

    assert (
        dashboard.calendar.year
        == 2026
    )

    assert len(
        dashboard.events
    ) == 2

    assert (
        dashboard.events[1].all_day
        is True
    )
