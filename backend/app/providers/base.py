from abc import ABC, abstractmethod
from datetime import datetime

from app.models.dashboard import CalendarEvent


class CalendarProvider(ABC):
    @abstractmethod
    def get_events(
        self,
        start: datetime,
        end: datetime,
    ) -> list[CalendarEvent]:
        """
        Return calendar events within the requested time window.
        """
        raise NotImplementedError
