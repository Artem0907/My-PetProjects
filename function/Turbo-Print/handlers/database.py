from tortoise import Model, Tortoise, fields

from ...settings import get_settings
from ..formatters.base import BaseFormatter
from ..levels import LogLevels, LogLevelStructure
from ..record import LogRecord
from .base import BaseHandler


class LogRecordModel(Model):
    id = fields.IntField(True)
    date = fields.DateField()
    time = fields.TimeField()
    logger_name = fields.CharField(50)
    level_name = fields.CharField(20)
    level_value = fields.IntField()
    message = fields.TextField()
    module = fields.CharField(255, null=True)
    function = fields.CharField(255, null=True)
    line_no = fields.IntField(null=True)
    extra = fields.JSONField(default={})  # type: ignore

    class Meta:  # pyright: ignore[reportIncompatibleVariableOverride]
        table = "user_messages"
        table_description = ""


class DatabaseHandler(BaseHandler):
    def __init__(
        self,
        db_url: str = "sqlite://logs.db",
        min_level: LogLevelStructure = LogLevels.NOTSET,
        formatter: BaseFormatter | None = None,
    ):
        super().__init__(min_level, formatter)
        self.db_url = db_url
        self.database = Tortoise()

    async def emit(self, record: LogRecord) -> None:
        await self.database.init(
            db_url=get_settings().database.url,
            modules={"models": [__name__]},
            use_tz=False,
            timezone=get_settings().timezone,
        )
        await self.database.generate_schemas()
        await LogRecordModel.create(
            date=record.date_time,
            time=record.date_time,
            logger_name=record.logger.get_name(),
            level_name=record.level.name,
            level_value=record.level.level,
            message=record.message,
            module=record.module,
            function=record.function,
            line_no=record.line_no,
            extra=record.extra,
        )
        await self.database.close_connections()
