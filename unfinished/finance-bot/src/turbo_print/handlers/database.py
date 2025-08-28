from tortoise import Tortoise

from ...models import LogRecordModel
from ..formatters.base import BaseFormatter
from ..levels import LogLevels, LogLevelStructure
from ..record import LogRecord
from .base import BaseHandler


class DatabaseHandler(BaseHandler):
    def __init__(
        self,
        database_tortoise_connection: Tortoise,
        min_level: LogLevelStructure = LogLevels.NOTSET,
        formatter: BaseFormatter | None = None,
    ):
        super().__init__(min_level, formatter)
        self.db = database_tortoise_connection

    async def emit(self, record: LogRecord) -> None:
        await LogRecordModel.create(
            datetime=record.date_time,
            logger_name=record.logger.get_name(),
            level_name=record.level.name,
            level_value=record.level.level,
            message=record.message,
            module=record.module,
            function=record.function,
            line_no=record.line_no,
            extra=record.extra,
        )
