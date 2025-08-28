from abc import ABC, abstractmethod

from src.turbo_print.record import LogRecord


class BaseMiddleware(ABC):
    @abstractmethod
    async def pre_process(self, record: LogRecord) -> None: ...
    @abstractmethod
    async def post_process(self, record: LogRecord) -> None: ...
