from contextvars import ContextVar
from datetime import datetime
from typing import Any, overload

from .filters.base import BaseFilter
from .formatters.base import BaseFormatter
from .formatters.simple import SimpleFormatter
from .handlers.base import BaseHandler
from .levels import LogLevels, LogLevelStructure
from .middlewares.base import BaseMiddleware
from .record import LogRecord


class _TurboLoggerMethods:
    _context: dict[str, Any]
    _global_context: dict[str, Any]
    _filters: list[BaseFilter]
    _formatter: BaseFormatter
    _handlers: list[BaseHandler]
    _level: LogLevelStructure
    _middlewares: list[BaseMiddleware]
    _name: str

    def get_name(self) -> str:
        return self._name

    def add_handler(self, handler: BaseHandler) -> None:
        self._handlers.append(handler)

    def remove_handler(self, handler: BaseHandler) -> None:
        self._handlers.remove(handler)

    def get_handlers(self) -> list[BaseHandler]:
        return self._handlers.copy()

    def reset_handlers(self) -> None:
        self._handlers.clear()

    def add_filter(self, filter: BaseFilter) -> None:
        self._filters.append(filter)

    def remove_filter(self, filter: BaseFilter) -> None:
        self._filters.remove(filter)

    def get_filters(self) -> list[BaseFilter]:
        return self._filters.copy()

    def reset_filters(self) -> None:
        self._filters.clear()

    def add_middleware(self, middleware: BaseMiddleware) -> None:
        self._middlewares.append(middleware)

    def remove_middleware(self, middleware: BaseMiddleware) -> None:
        self._middlewares.remove(middleware)

    def get_middlewares(self) -> list[BaseMiddleware]:
        return self._middlewares.copy()

    def reset_middlewares(self) -> None:
        self._middlewares.clear()

    def set_formatter(self, formatter: BaseFormatter) -> None:
        self._formatter = formatter

    def get_formatter(self) -> BaseFormatter:
        return self._formatter

    def set_level(self, level: LogLevelStructure) -> None:
        self._level = level

    def get_level(self) -> LogLevelStructure:
        return self._level

    def add_global_context(self, **context: Any) -> None:
        self._global_context.update(**context)

    def remove_global_context(self, context_name: str) -> None:
        del self._global_context[context_name]

    @overload
    def get_global_context(self, context_name: str) -> Any: ...

    @overload
    def get_global_context(self) -> dict[str, Any]: ...

    def get_global_context(
        self, context_name: str | None = None
    ) -> dict[str, Any] | Any:
        if context_name:
            return self._global_context.get(context_name)
        return self._global_context.copy()

    def reset_global_context(self) -> None:
        self._global_context.clear()

    def add_context(self, **context: Any) -> None:
        self._context.update(**context)

    def remove_context(self, context_name: str) -> None:
        del self._context[context_name]

    @overload
    def get_context(self, context_name: str) -> Any: ...

    @overload
    def get_context(self) -> dict[str, Any]: ...

    def get_context(
        self, context_name: str | None = None
    ) -> dict[str, Any] | Any:
        if context_name:
            return self._context.get(context_name)
        return self._context.copy()

    def reset_context(self) -> None:
        self._context.clear()


class TurboLogger(_TurboLoggerMethods):
    root_logger: ContextVar["TurboLogger"] = ContextVar(
        "TurboPrint_root_logger", default=None  # type: ignore[arg-type]
    )  # pyright: ignore[reportAssignmentType]
    _loggers: dict[str, "TurboLogger"] = {}
    _global_context: dict[str, Any] = {}

    @classmethod
    def get_all_loggers(cls) -> dict[str, "TurboLogger"]:
        return cls._loggers.copy()

    @classmethod
    def get_logger(cls, name: str = "root") -> "TurboLogger":
        if name == "root":
            if not cls.root_logger.get():
                cls.root_logger.set(TurboLogger("root"))
            return cls.root_logger.get()

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
        /,
        handlers: list[BaseHandler] | None = None,
        filters: list[BaseFilter] | None = None,
        middlewares: list[BaseMiddleware] | None = None,
        context: dict[str, Any] | None = None,
        inheritance: bool = True,
        propagate: bool = True,
    ):
        if not self.root_logger.get() and name == "root":
            self.root_logger.set(self)
        elif not self.root_logger.get() and name != "root":
            self.root_logger.set(TurboLogger("root"))

        if name != "root":
            self._loggers[name] = self
            _parent_name = name.rsplit(".", 1)[0]
            if _parent_name == name or _parent_name == "root":
                self.parent = self.get_logger("root")
            else:
                self.parent = self.get_logger(_parent_name)
        else:
            self.parent = None  # type: ignore[assignment]

        if inheritance and self.parent:
            self._name = name
            self._level: LogLevelStructure = (
                min_level or self.parent.get_level()
            )
            self._handlers: list[BaseHandler] = (
                handlers or self.parent.get_handlers()
            )
            self._filters: list[BaseFilter] = (
                filters or self.parent.get_filters()
            )
            self._middlewares: list[BaseMiddleware] = (
                middlewares or self.parent.get_middlewares()
            )
            self._formatter: BaseFormatter = (
                formatter or self.parent.get_formatter()
            )
            self._context: dict[str, Any] = context or self.parent.get_context()
            self._propagate: bool = propagate
        else:
            self._name = name
            self._level: LogLevelStructure = min_level or LogLevels.INFO  # type: ignore[no-redef]
            self._handlers: list[BaseHandler] = handlers or []  # type: ignore[no-redef]
            self._filters: list[BaseFilter] = filters or []  # type: ignore[no-redef]
            self._middlewares: list[BaseMiddleware] = middlewares or []  # type: ignore[no-redef]
            self._formatter: BaseFormatter = formatter or SimpleFormatter()  # type: ignore[no-redef]
            self._context: dict[str, Any] = context or {}  # type: ignore[no-redef]
            self._propagate: bool = propagate  # type: ignore[no-redef]

    async def log(
        self,
        level: LogLevelStructure,
        message: str,
        /,
        module: str | None = None,
        function: str | None = None,
        line_no: int | None = None,
        **extra: Any,
    ) -> None:
        record = LogRecord(
            message,
            level,
            self,
            datetime.now(),
            {**self.get_context(), **extra},
            module,
            function,
            line_no,
        )

        filters = [
            (await filter.filter(record)) for filter in self.get_filters()
        ]

        if level.level >= self._level.level and all(filters):
            try:
                for middleware in self.get_middlewares():
                    await middleware.pre_process(record)
                for handler in self.get_handlers():
                    await handler.handle(record)
                for middleware in reversed(self.get_middlewares()):
                    await middleware.post_process(record)
            except Exception as exception:
                for middleware in reversed(self.get_middlewares()):
                    await middleware.error_process(exception, record)
