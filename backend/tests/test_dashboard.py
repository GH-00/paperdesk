from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_dashboard():
    response = client.get(
        "/api/v1/dashboard"
    )

    assert response.status_code == 200

    body = response.json()

    assert "generated_at" in body
    assert "device" in body
    assert "calendar" in body
    assert "events" in body
    assert "ddays" in body
    assert "environment" in body

    assert (
        body["device"]["name"]
        == "paperdesk-test"
    )

    assert (
        body["device"]["timezone"]
        == "Asia/Seoul"
    )

    assert (
        body["environment"]["source"]
        == "mock"
    )


def test_dashboard_event_schema():
    response = client.get(
        "/api/v1/dashboard"
    )

    assert response.status_code == 200

    events = response.json()[
        "events"
    ]

    assert len(events) >= 1

    event = events[0]

    assert "id" in event
    assert "title" in event
    assert "start" in event
    assert "end" in event
    assert "all_day" in event


def test_dashboard_uses_mock_calendar():
    response = client.get(
        "/api/v1/dashboard"
    )

    assert response.status_code == 200

    titles = [
        event["title"]
        for event in response.json()["events"]
    ]

    assert "Team Meeting" in titles
    assert "English Class" in titles
    assert "Project Review" in titles
