from datetime import date, datetime

from pydantic import BaseModel


class DeviceInfo(BaseModel):
    name: str
    timezone: str


class CalendarInfo(BaseModel):
    year: int
    month: int
    today: int


class CalendarEvent(BaseModel):
    id: str
    title: str
    start: datetime
    end: datetime
    all_day: bool = False


class DDay(BaseModel):
    title: str
    date: date
    days_remaining: int


class Environment(BaseModel):
    temperature: float
    humidity: float
    source: str


class Dashboard(BaseModel):
    generated_at: datetime
    device: DeviceInfo
    calendar: CalendarInfo
    events: list[CalendarEvent]
    ddays: list[DDay]
    environment: Environment
