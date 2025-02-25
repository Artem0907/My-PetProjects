from datetime import datetime
from enum import Enum
from os import makedirs
from typing import Any, Callable, Literal, Optional, Self, TypedDict
from os.path import join, exists, abspath, dirname
from colorama import Fore, Style

# from logging import Formatter, Handler, Filter


class LogLevels(Enum):
    """
    Описывает уровни логирования
    """

    NOTSET = 0
    SUCCESS = 1
    INFO = 2
    LOG = 3
    DEBUG = 4
    WARNING = WARN = 5
    ERROR = 6
    FATAL = CRITICAL = 7

    @property
    def color(self):
        return {
            self.NOTSET: Fore.WHITE,
            self.SUCCESS: Fore.GREEN,
            self.INFO: Fore.BLUE,
            self.LOG: Fore.LIGHTCYAN_EX,
            self.DEBUG: Fore.LIGHTMAGENTA_EX,
            self.WARNING: Fore.LIGHTYELLOW_EX,
            self.ERROR: Fore.LIGHTRED_EX,
            self.FATAL: Fore.LIGHTRED_EX + Style.BRIGHT,
        }[self]


class TurboPrint_Output(TypedDict):
    """
    Описывает структуру выходных данных: файл, консоль и текст.
    """

    standard_console: str
    colored_console: str
    standard_file: str
    standard_output: str
    colored_output: str


class FilterData(TypedDict):
    message: Optional[str]
    level: LogLevels
    prefix: Optional[str]
    date_time: datetime
    parent: Optional[object]


class TurboPrint_Handler(object):
    def emit(self, record: dict[str, Any]):
        raise NotImplementedError("emit must be implemented by Handler subclasses")

    def close(self) -> None:
        return

    def flush(self) -> None:
        return


class TurboPrint_Filter(object):
    def filter(self, record: FilterData) -> bool:
        raise NotImplementedError("filter must be implemented by Filter subclasses")


class TurboPrint_Formatter(object):
    def file_format(self, record: dict[str, Any]) -> str:
        raise NotImplementedError(
            "file format must be implemented by Formatter subclasses"
        )

    def console_format(self, record: dict[str, Any]) -> str:
        raise NotImplementedError(
            "console format must be implemented by Formatter subclasses"
        )

    def output_format(self, record: dict[str, Any]) -> str:
        raise NotImplementedError(
            "output format must be implemented by Formatter subclasses"
        )


class TurboPrint:
    """
    Класс для удобного вывода логов с возможностью цветного выделения и записи в файл
    """

    Handler = TurboPrint_Handler
    Filter = TurboPrint_Filter
    Formatter = TurboPrint_Formatter
    DEFAULT_FORMAT = "[{time}] {prefix} | {level}: {message}"

    def __init__(
        self,
        *,
        # handler: Optional[Handler] = None,
        console_format: str = DEFAULT_FORMAT,
        console_log_level: LogLevels = LogLevels.INFO,
        console_output: bool = True,
        directory: Optional[str] = "logs",
        enable: bool = True,
        file_format: str = DEFAULT_FORMAT,
        file_log_level: LogLevels = LogLevels.WARNING,
        file_name: Optional[str] = None,
        file_output: bool = True,
        filters: Optional[list[Filter]] = None,
        formatter: Optional[Formatter] = None,
        output_format: str = DEFAULT_FORMAT,
        parent: Optional[Self] = None,
        prefix: str = "TP",
    ) -> None:
        """
        Инициализирует объект TurboPrint

        Args:
            # handlers: Список обработчиков лога.
            console_format: Формат вывода лога в консоль.
            console_log_level: Минимальный уровень логирования для вывода в консоль.
            console_output: Вывод лога в консоль.
            directory: Директория для сохранения лог-файлов.
            enable: Включить/выключить запись логов.
            file_format: Формат записи лога в файл.
            file_log_level: Минимальный уровень логирования для записи в файл.
            file_name: Имя файла для логов (без расширения).
            file_output: Запись лога в файл.
            filters: Список фильтров лога.
            formatter: Формат лога.
            output_format: Формат возвращаемого лога.
            parent: Родитель логера.
            prefix: Префикс для сообщений в логах.
        """
        self.filters: list[TurboPrint_Filter] = []
        if filters:
            self.filters += filters
        if parent and parent.filters:
            self.filters += parent.filters
        # self.handlers = handlers

        self.console_format = formatter or console_format
        self.console_log_level = console_log_level
        self.console_output = console_output
        self.enable = enable
        self.file_format = file_format
        self.file_log_level = file_log_level
        self.file_output = file_output
        self.output_format = output_format
        self.parent = parent
        self.prefix = prefix

        log_path = (
            abspath(join(dirname(__file__), directory))
            if directory
            else abspath(dirname(__file__))
        )
        makedirs(log_path, exist_ok=True)
        self.date = datetime.now().strftime("%Y-%m-%d")
        file_name = f"{self.date}__{file_name}.log" if file_name else f"{self.date}.log"
        self.file_path = abspath(join(log_path, file_name))

    def __call__(
        self,
        message: Optional[str] = None,
        level: LogLevels = LogLevels.NOTSET,
        color: Optional[str] = None,
        **kwargs: Any,
    ) -> TurboPrint_Output | Literal[False]:
        """
        Записывает сообщение в лог.

        Args:
            message: Сообщение для записи.
            level: Уровень сообщения.
            color: Цвет для сообщения (переопределяет стандартный цвет уровня).
        Returns:
            Отформатированное сообщение.
        """
        date_time = datetime.now()
        format_data = FilterData(
            message=message,
            level=level,
            prefix=self.prefix,
            date_time=date_time,
            parent=self.parent,
        )

        if not all(
            map(
                lambda filter: filter.filter(format_data),
                set(self.filters),
            )
        ):
            return False

        formatted_message = self._format_message(
            date_time, message, level, color, **kwargs
        )

        if not self.enable:
            return formatted_message

        if self.file_output and level.value >= self.file_log_level.value:
            try:
                if not exists(dirname(self.file_path)):
                    makedirs(dirname(self.file_path), exist_ok=True)
                with open(self.file_path, "a+", encoding="utf-8") as file:
                    file.write(formatted_message["standard_file"] + "\n")
            except Exception as e:
                print(f"Ошибка записи в лог файл: {e}")

        if self.console_output and level.value >= self.console_log_level.value:
            print(formatted_message["colored_console"])
        return formatted_message

    def _format_message(
        self,
        date_time: datetime,
        message: Optional[str],
        level: LogLevels,
        color: Optional[str],
        **kwargs: Any,
    ) -> TurboPrint_Output:
        """
        Форматирует сообщение для вывода.
        """

        format_data = {
            "level": level.name,
            "message": message,
            "prefix": self.prefix,
            "time": date_time.strftime("%H:%M:%S"),
            **kwargs,
        }

        standard_console_message = (
            self.console_format.console_format(**format_data)
            if isinstance(self.console_format, self.Formatter)
            else self.console_format.format(**format_data)
        )
        colored_console_message = (
            Style.RESET_ALL
            + (color or level.color)
            + standard_console_message
            + Style.RESET_ALL
        )

        standard_file_message = (
            self.file_format.file_format(**format_data)
            if isinstance(self.file_format, self.Formatter)
            else self.file_format.format(**format_data)
        )

        standard_output_message = (
            self.output_format.output_format(**format_data)
            if isinstance(self.output_format, self.Formatter)
            else self.output_format.format(**format_data)
        )
        colored_output_message = (
            Style.RESET_ALL
            + (color or level.color)
            + standard_output_message
            + Style.RESET_ALL
        )

        return TurboPrint_Output(
            standard_console=standard_console_message,
            colored_console=colored_console_message,
            standard_file=standard_file_message,
            standard_output=standard_output_message,
            colored_output=colored_output_message,
        )

    def exception[_F: Callable](self, func: _F) -> _F:  # type: ignore[type-arg]
        """
        Записывает информацию об исключении в лог.
        """

        def wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                return func(*args, **kwargs)
            except Exception as e:
                self(
                    f'[{type(e).__name__}] {e} ["{func.__code__.co_filename}:{func.__code__.co_firstlineno}"]',
                    level=LogLevels.ERROR,
                )

        return wrapper  # type: ignore[return-value]


if __name__ == "__main__":
    tp = TurboPrint(
        console_format="[{prefix}] {level}: {message}",
        console_log_level=LogLevels.DEBUG,
        console_output=True,
        directory="logs",
        enable=True,
        file_format="[{time}] {prefix} | {level}: {message}",
        file_log_level=LogLevels.WARN,
        file_name="my_app",
        file_output=True,
        filters=None,
        formatter=None,
        parent=None,
        prefix="TEST",
    )

    tp.console_log_level = tp.file_log_level = LogLevels.NOTSET

    tp("test message", LogLevels.NOTSET)
    tp("test message", LogLevels.SUCCESS)
    tp("test message", LogLevels.INFO)
    tp("test message", LogLevels.LOG)
    tp("test message", LogLevels.DEBUG)
    tp("test message", LogLevels.WARN)
    tp("test message", LogLevels.WARNING)
    tp("test message", LogLevels.ERROR)
    tp("test message", LogLevels.CRITICAL)
    tp("test message", LogLevels.FATAL)

    print("{")
    for level in LogLevels._member_map_.values():
        print(
            "  "
            + level.color  # type: ignore
            + level.name
            + Style.RESET_ALL
            + f": {level.value},"
        )
    print("}")
