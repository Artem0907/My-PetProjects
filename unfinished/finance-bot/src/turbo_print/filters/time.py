from datetime import time
from typing import Literal

from ..record import LogRecord
from .base import BaseFilter


class TimeFilter(BaseFilter):
    def __init__(
        self,
        start: time | None = None,
        end: time | None = None,
        weekdays: (
            set[
                Literal[
                    "monday",
                    "tuesday",
                    "wednesday",
                    "thursday",
                    "friday",
                    "saturday",
                    "sunday",
                ]
            ]
            | None
        ) = None,
        inverse: bool = False,
    ) -> None:
        self.start = start
        self.end = end
        self.weekdays = weekdays
        self.inverse = inverse

    async def filter(self, record: LogRecord) -> bool:
        current_time = record.date_time.time()

        if self.weekdays:
            current_weekday = record.date_time.weekday()
            weekdays = []
            for weekday in self.weekdays:
                weekdays.append(
                    [
                        "monday",
                        "tuesday",
                        "wednesday",
                        "thursday",
                        "friday",
                        "saturday",
                        "sunday",
                    ].index(weekday)
                )
            in_weekday = current_weekday in weekdays
        else:
            in_weekday = True

        if self.start is None and self.end is not None:
            in_timerange = current_time <= self.end
        elif self.end is None and self.start is not None:
            in_timerange = current_time >= self.start
        elif self.start is not None and self.end is not None:
            if self.start <= self.end:
                in_timerange = self.start <= current_time <= self.end
            else:
                in_timerange = (
                    current_time >= self.start or current_time <= self.end
                )
        else:
            in_timerange = True

        result = in_weekday and in_timerange
        return not result if self.inverse else result
