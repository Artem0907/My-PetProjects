from abc import ABC, abstractmethod

from ..record import LogRecord


class BaseFilter(ABC):
    @abstractmethod
    async def filter(self, record: LogRecord) -> bool:
        pass
