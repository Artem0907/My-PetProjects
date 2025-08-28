from typing import Literal

from ..record import LogRecord
from .base import BaseFilter


class CompositeFilter(BaseFilter):
    def __init__(
        self,
        filters: list[BaseFilter],
        mode: Literal["any", "all"] = "all",
        inverse: bool = False,
    ) -> None:
        self.filters = filters
        self.mode = mode
        self.inverse = inverse

    async def filter(self, record: LogRecord) -> bool:
        filters_result = [
            (await filter.filter(record)) for filter in self.filters
        ]
        if self.mode == "all":
            return all(filters_result) ^ self.inverse
        elif self.mode == "any":
            return any(filters_result) ^ self.inverse
        else:
            return self.inverse  # type: ignore[unreachable]
