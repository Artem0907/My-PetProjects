from abc import ABC, abstractmethod

from ..record import LogRecord


class BaseFilter(ABC):
    @abstractmethod
    def filter(self, record: LogRecord) -> bool:
        pass

    def __call__(self, record: LogRecord) -> bool:
        return self.filter(record)
