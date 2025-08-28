from re import compile as re_compile
from typing import Literal

from ..record import LogRecord
from .base import BaseFilter


class RegexFilter(BaseFilter):
    def __init__(
        self,
        pattern: str,
        field: (
            Literal["logger_name", "message", "level", "module", "function"]
            | str
        ) = "message",
        inverse: bool = False,
    ):
        self.pattern = re_compile(pattern)
        self.field = field
        self.inverse = inverse

    async def filter(self, record: LogRecord) -> bool:
        if self.field == "message":
            result = self.pattern.match(record.message) is not None
        elif self.field == "logger_name":
            result = self.pattern.match(record.logger.get_name()) is not None
        elif self.field == "level":
            result = self.pattern.match(record.level.name) is not None
        elif self.field == "module":
            if record.module:
                result = self.pattern.match(record.module) is not None
            else:
                result = False
        elif self.field == "function":
            if record.function:
                result = self.pattern.match(record.function) is not None
            else:
                result = False
        else:
            value = record.extra.get(self.field, "")
            result = bool(self.pattern.search(str(value)))
        return not result if self.inverse else result
