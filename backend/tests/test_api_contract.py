from datetime import datetime

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def get_dashboard():
    response = client.get("/api/v1/dashboard")

    assert response.status_code == 200

    return response.json()


def test_dashboard_contract_top_level():
    body = get_dashboard()

    assert set(body.keys()) == {
        "generated_at",
        "device",
        "calendar",
        "events",
        "ddays",
        "environment",
    }


def test_generated_at_is_iso8601():
    body = get_dashboard()

    parsed = datetime.fromisoformat(
        body["generated_at"]
    )

    assert parsed.tzinfo is not None


def test_device_contract():
    device = get_dashboard()["device"]

    assert set(device.keys()) == {
        "name",
        "timezone",
    }

    assert isinstance(
        device["name"],
        str,
    )

    assert isinstance(
        device["timezone"],
        str,
    )


def test_calendar_contract():
    calendar = get_dashboard()["calendar"]

    assert set(calendar.keys()) == {
        "year",
        "month",
        "today",
    }

    assert isinstance(
        calendar["year"],
        int,
    )

    assert (
        1
        <= calendar["month"]
        <= 12
    )

    assert (
        1
        <= calendar["today"]
        <= 31
    )


def test_event_contract():
    events = get_dashboard()["events"]

    assert isinstance(events, list)

    for event in events:
        assert set(event.keys()) == {
            "id",
            "title",
            "start",
            "end",
            "all_day",
        }

        assert isinstance(
            event["id"],
            str,
        )

        assert isinstance(
            event["title"],
            str,
        )

        assert isinstance(
            event["all_day"],
            bool,
        )

        start = datetime.fromisoformat(
            event["start"]
        )

        end = datetime.fromisoformat(
            event["end"]
        )

        assert (
            start.tzinfo is not None
        )

        assert (
            end.tzinfo is not None
        )

        assert end >= start


def test_dday_contract():
    ddays = get_dashboard()["ddays"]

    assert isinstance(ddays, list)

    for dday in ddays:
        assert set(dday.keys()) == {
            "title",
            "date",
            "days_remaining",
        }

        assert isinstance(
            dday["title"],
            str,
        )

        assert isinstance(
            dday["days_remaining"],
            int,
        )


def test_environment_contract():
    environment = get_dashboard()[
        "environment"
    ]

    assert set(environment.keys()) == {
        "temperature",
        "humidity",
        "source",
    }

    assert isinstance(
        environment["temperature"],
        (int, float),
    )

    assert isinstance(
        environment["humidity"],
        (int, float),
    )

    assert isinstance(
        environment["source"],
        str,
    )
