from sys import stdout as default_output
from typing import TextIO

from ..formatters.base import BaseFormatter
from ..levels import LogLevels, LogLevelStructure
from ..record import LogRecord
from .base import BaseHandler


class StreamHandler(BaseHandler):
    def __init__(
        self,
        stream: TextIO = default_output,
        min_level: LogLevelStructure = LogLevels.NOTSET,
        formatter: BaseFormatter | None = None,
    ) -> None:
        super().__init__(min_level, formatter)
        self.stream = stream

    async def emit(self, record: LogRecord) -> None:
        formatter = self.formatter or record.logger.get_formatter()
        self.stream.write(formatter.format(record) + "\n")
        self.stream.flush()
