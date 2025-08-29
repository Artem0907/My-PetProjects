from datetime import datetime
from typing import TYPE_CHECKING, Any, TypedDict

from colorama import Fore, Style

from ..levels import LogLevelStructure
from ..record import LogRecord
from .base import BaseFormatter

if TYPE_CHECKING:
    from ..logger import TurboLogger


class RecordFormatterDict(TypedDict):
    message: str
    level_name: str
    level_value: int
    level: LogLevelStructure
    logger: "TurboLogger"
    logger_name: str
    prefix: str
    date: str
    time: str
    datetime: datetime
    module: str | None
    function: str | None
    line_no: int | None


class SimpleFormatter(BaseFormatter):
    def __init__(
        self,
        simple_format: str = "[{date} {time}] {prefix} | {level_name}: {message}",
        date_format: str = "%d/%m/%Y",
        time_format: str = "%H:%M:%S",
        colored: bool = False,
    ):
        self.simple_format = simple_format
        self.date_format = date_format
        self.time_format = time_format
        self.colored = colored

    def format(self, record: LogRecord) -> str:
        level_color = record.level.color or Fore.RESET

        extra: dict[str, Any] = {}
        for key, value in record.extra.items():
            if "__repr__" in dir(value):
                extra[key] = value
            elif "__str__" in dir(value) and "__repr__" not in dir(value):
                value.__repr__ = value.__str__
                extra[key] = value
            else:
                continue

        record_format = RecordFormatterDict(
            message=record.message,
            level_name=record.level.name,
            level_value=record.level.level,
            level=record.level,
            logger=record.logger,
            logger_name=record.logger.get_name(),
            prefix=record.logger.get_name(),
            date=record.date_time.strftime(self.date_format),
            time=record.date_time.strftime(self.time_format),
            datetime=record.date_time,
            module=record.module,
            function=record.function,
            line_no=record.line_no,
        )
        output = self.simple_format.format(**record_format, **extra)
        if self.colored:
            return f"{level_color}{output}{Style.RESET_ALL}"
        return output
