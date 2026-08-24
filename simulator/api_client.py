import httpx

from simulator.config import API_URL


def fetch_dashboard() -> dict:
    response = httpx.get(
        API_URL,
        timeout=5.0,
    )

    response.raise_for_status()

    return response.json()
