from datetime import datetime
from enum import Enum
from os import makedirs
from typing import Any, Callable, Optional, TypedDict
from os.path import join, exists, abspath, dirname
from colorama import Fore, Style
from logging import Formatter, Handler, Filter


class TurboPrint_Handler:
    def __init__(self, *args): ...
    def emit(self, record): ...
    def close(self): ...
    def flush(self): ...


class TurboPrint_Filter:
    def __init__(self, *args): ...
    def filter(self, record) -> bool: ...


class TurboPrint_Formatter:
    def __init__(self, *args): ...
    def format(self, record) -> str: ...


class TurboPrintOutput(TypedDict):
    """
    Описывает структуру выходных данных: файл, цветная консоль или текст.
    """

    file: str
    console: str
    standard: str


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


class TurboPrint:
    """
    Класс для удобного вывода логов с возможностью цветного выделения и записи в файл
    """

    Handler = TurboPrint_Handler
    Filter = TurboPrint_Filter
    Formatter = TurboPrint_Formatter

    def __init__(
        self,
        *,
        console_format: str = "[{time}] {prefix} | {level}: {message}",
        console_log_level: LogLevels = LogLevels.INFO,
        console_output: bool = True,
        directory: Optional[str] = "logs",
        enable: bool = True,
        file_format: str = "[{time}] {prefix} | {level}: {message}",
        file_log_level: LogLevels = LogLevels.WARNING,
        file_name: Optional[str] = None,
        file_output: bool = True,
        prefix: str = "TP",
    ) -> None:
        """
        Инициализирует объект TurboPrint

        Args:
            console_format: Формат вывода лога в консоль.
            console_log_level: Минимальный уровень логирования для вывода в консоль.
            console_output: Вывод лога в консоль.
            directory: Директория для сохранения лог-файлов.
            enable: Включить/выключить запись логов.
            file_format: Формат записи лога в файл.
            file_log_level: Минимальный уровень логирования для записи в файл.
            file_name: Имя файла для логов (без расширения).
            file_output: Запись лога в файл.
            prefix: Префикс для сообщений в логах.
        """

        self.console_format = console_format
        self.console_log_level = console_log_level
        self.console_output = console_output
        self.enable = enable
        self.file_format = file_format
        self.file_log_level = file_log_level
        self.file_output = file_output
        self.prefix = prefix

        log_path = (
            abspath(join(dirname(__file__), directory))
            if directory
            else abspath(dirname(__file__))
        )
        makedirs(log_path, exist_ok=True)
        self.date = datetime.now().strftime("%d-%m-%Y")
        file_name = f"{self.date}__{file_name}.log" if file_name else f"{self.date}.log"
        self.file_path = abspath(join(log_path, file_name))

    def __call__(
        self,
        message: Optional[str] = None,
        level: LogLevels = LogLevels.NOTSET,
        color: Optional[str] = None,
        **kwargs: Any,
    ) -> TurboPrintOutput:
        """
        Записывает сообщение в лог.

        Args:
            message: Сообщение для записи.
            level: Уровень сообщения.
            color: Цвет для сообщения (переопределяет стандартный цвет уровня).
        Returns:
            Отформатированное сообщение.
        """

        if not self.enable:
            return self._format_message(message, level, color, **kwargs)

        formatted_message = self._format_message(message, level, color, **kwargs)

        if self.file_output and level.value >= self.file_log_level.value:
            try:
                if not exists(dirname(self.file_path)):
                    makedirs(dirname(self.file_path), exist_ok=True)
                with open(self.file_path, "a+", encoding="utf-8") as file:
                    file.write(formatted_message["file"] + "\n")
            except Exception as e:
                print(f"Ошибка записи в лог файл: {e}")

        if self.console_output and level.value >= self.console_log_level.value:
            print(formatted_message["console"])
        return formatted_message

    def _format_message(
        self,
        message: Optional[str],
        level: LogLevels,
        color: Optional[str],
        **kwargs: Any,
    ) -> TurboPrintOutput:
        """
        Форматирует сообщение для вывода.
        """

        format_data = {
            "level": level.name,
            "message": message,
            "prefix": self.prefix,
            "time": datetime.now().strftime("%H:%M:%S"),
            **kwargs,
        }

        standard_message = self.console_format.format(**format_data)
        colored_console_message = (
            Style.RESET_ALL
            + (color or level.color)
            + standard_message
            + Style.RESET_ALL
        )

        standard_file_message = self.file_format.format(**format_data)

        return TurboPrintOutput(
            standard=standard_message,
            console=colored_console_message,
            file=standard_file_message,
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
