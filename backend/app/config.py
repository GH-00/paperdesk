from pathlib import Path
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


APP_DIR = Path(__file__).resolve().parent
BACKEND_DIR = APP_DIR.parent


class Settings(BaseSettings):
    app_env: str = "development"

    timezone: str = "Asia/Seoul"
    device_name: str = "paperdesk-dev"

    calendar_provider: Literal["mock", "google"] = "mock"

    dday_title: str = "Demo Day"
    dday_date: str | None = None

    mock_temperature: float = 26.4
    mock_humidity: float = 52.0

    model_config = SettingsConfigDict(
        env_file=BACKEND_DIR / ".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


settings = Settings()
