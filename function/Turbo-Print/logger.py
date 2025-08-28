from asyncio import get_event_loop, run_coroutine_threadsafe
from datetime import datetime
from typing import Any

from .filters.base import BaseFilter
from .formatters.base import BaseFormatter
from .formatters.simple import SimpleFormatter
from .handlers.base import BaseHandler
from .levels import LogLevels, LogLevelStructure
from .record import LogRecord


class _TurboLoggerMethods:
    _name: str
    _handlers: list[BaseHandler]
    _filters: list[BaseFilter]
    _formatter: BaseFormatter
    _level: LogLevelStructure

    def get_name(self) -> str:
        return self._name

    def add_handler(self, handler: BaseHandler) -> None:
        self._handlers.append(handler)

    def remove_handler(self, handler: BaseHandler) -> None:
        self._handlers.remove(handler)

    def get_handlers(self) -> list[BaseHandler]:
        return self._handlers.copy()

    def add_filter(self, filter: BaseFilter) -> None:
        self._filters.append(filter)

    def remove_filter(self, filter: BaseFilter) -> None:
        self._filters.remove(filter)

    def get_filters(self) -> list[BaseFilter]:
        return self._filters.copy()

    def set_formatter(self, formatter: BaseFormatter) -> None:
        self._formatter = formatter

    def get_formatter(self) -> BaseFormatter:
        return self._formatter

    def set_level(self, level: LogLevelStructure) -> None:
        self._level = level

    def get_level(self) -> LogLevelStructure:
        return self._level


class TurboLogger(_TurboLoggerMethods):
    root_logger: "TurboLogger" = None  # type: ignore
    _loggers: dict[str, "TurboLogger"] = {}

    @classmethod
    def get_all_loggers(cls) -> dict[str, "TurboLogger"]:
        return cls._loggers.copy()

    @classmethod
    def get_logger(cls, name: str = "root") -> "TurboLogger":
        if name == "root":
            if not cls.root_logger:
                cls.root_logger = TurboLogger("root")
            return cls.root_logger

        if name in cls._loggers:
            return cls._loggers[name]
        else:
            logger = TurboLogger(name)
            return logger

    def __init__(
        self,
        name: str = "root",
        min_level: LogLevelStructure | None = None,
        formatter: BaseFormatter | None = None,
        handlers: list[BaseHandler] | None = None,
        filters: list[BaseFilter] | None = None,
        inheritance: bool = True,
        propagate: bool = True,
    ):
        if not self.root_logger and name == "root":
            self.root_logger = self
        elif not self.root_logger and name != "root":
            self.root_logger = TurboLogger("root")

        if name != "root":
            self._loggers[name] = self
            _parent_name = name.rsplit(".", 1)[0]
            if _parent_name == name or _parent_name == "root":
                self.parent = self.get_logger("root")
            else:
                self.parent = self.get_logger(_parent_name)
        else:
            self.parent = None  # type: ignore

        if inheritance and self.parent:
            self._name = name
            self._level: LogLevelStructure = min_level or self.parent._level
            self._handlers: list[BaseHandler] = (
                handlers or self.parent._handlers
            )
            self._filters: list[BaseFilter] = filters or self.parent._filters
            self._formatter: BaseFormatter = formatter or self.parent._formatter
            self._propagate: bool = propagate
        else:
            self._name = name
            self._level: LogLevelStructure = min_level or LogLevels.INFO
            self._handlers: list[BaseHandler] = handlers or []
            self._filters: list[BaseFilter] = filters or []
            self._formatter: BaseFormatter = formatter or SimpleFormatter()
            self._propagate: bool = propagate

    def log(
        self,
        level: LogLevelStructure,
        message: str,
        /,
        module: str | None = None,
        function: str | None = None,
        line_no: int | None = None,
        **extra: Any,
    ) -> None:
        if level.level >= self._level.level:
            record = LogRecord(
                message,
                level,
                self,
                datetime.now(),
                extra,
                module,
                function,
                line_no,
            )
            for handler in self._handlers:
                run_coroutine_threadsafe(
                    handler.handle(record), get_event_loop()
                )

    async def async_log(
        self,
        level: LogLevelStructure,
        message: str,
        /,
        module: str | None = None,
        function: str | None = None,
        line_no: int | None = None,
        **extra: Any,
    ) -> None:
        if level.level >= self._level.level:
            record = LogRecord(
                message,
                level,
                self,
                datetime.now(),
                extra,
                module,
                function,
                line_no,
            )
            for handler in self._handlers:
                await handler.handle(record)
