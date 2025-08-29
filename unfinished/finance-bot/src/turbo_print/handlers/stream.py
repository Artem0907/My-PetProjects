from sys import stdout as default_output
from typing import TextIO

from colorama import Fore, Style

from ..formatters.base import BaseFormatter
from ..formatters.simple import SimpleFormatter
from ..levels import LogLevels, LogLevelStructure
from ..record import LogRecord
from .base import BaseHandler


class StreamHandler(BaseHandler):
    def __init__(
        self,
        stream: TextIO = default_output,
        min_level: LogLevelStructure = LogLevels.NOTSET,
        formatter: BaseFormatter | None = None,
        colored: bool = True,
    ) -> None:
        super().__init__(min_level, formatter)
        self.stream = stream
        self.colored = colored

    async def emit(self, record: LogRecord) -> None:
        formatter = self.formatter or record.logger.get_formatter()
        if isinstance(formatter, SimpleFormatter):
            formatter.colored = self.colored
            self.stream.write(formatter.format(record) + "\n")
            self.stream.flush()
        output = formatter.format(record)
        if self.colored:
            self.stream.write(output + "\n")
        else:
            level_color = record.level.color or Fore.RESET
            self.stream.write(f"{level_color}{output}{Style.RESET_ALL}" + "\n")
        self.stream.flush()
