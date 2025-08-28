import logging

from ..levels import LogLevels
from ..logger import TurboLogger


class TurboPrintLoggingHandler(logging.Handler):
    def __init__(self, level: int = logging.NOTSET):
        super().__init__(level)

    def emit(self, record: logging.LogRecord) -> None:
        level = {
            logging.DEBUG: LogLevels.DEBUG,
            logging.INFO: LogLevels.INFO,
            logging.WARNING: LogLevels.WARNING,
            logging.ERROR: LogLevels.ERROR,
            logging.CRITICAL: LogLevels.CRITICAL,
        }.get(record.levelno, LogLevels.NOTSET)

        logger = TurboLogger(record.name)
        logger.log(
            level,
            record.msg,
            module=record.module,
            function=record.funcName,
            line_no=record.lineno,
        )
