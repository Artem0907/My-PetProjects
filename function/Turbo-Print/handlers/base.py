from abc import ABC, abstractmethod

from ..formatters.base import BaseFormatter
from ..levels import LogLevels, LogLevelStructure
from ..record import LogRecord


class BaseHandler(ABC):
    def __init__(
        self,
        min_level: LogLevelStructure = LogLevels.NOTSET,
        formatter: BaseFormatter | None = None,
    ) -> None:
        self.level = min_level
        self.formatter = formatter

    async def handle(self, record: LogRecord) -> None:
        if record.level.level >= self.level.level:
            await self.emit(record)

    @abstractmethod
    async def emit(self, record: LogRecord) -> None:
        pass
