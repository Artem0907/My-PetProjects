from abc import ABC, abstractmethod

from ..record import LogRecord


class BaseFormatter(ABC):
    @abstractmethod
    def format(self, record: LogRecord) -> str:
        pass
