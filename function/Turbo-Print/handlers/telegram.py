from aiogram import Bot
from aiogram.utils.token import validate_token

from ..formatters.base import BaseFormatter
from ..levels import LogLevels, LogLevelStructure
from ..record import LogRecord
from .base import BaseHandler


class TelegramHandler(BaseHandler):
    def __init__(
        self,
        token_or_bot: str | Bot,
        chat_id: int | str,
        min_level: LogLevelStructure = LogLevels.NOTSET,
        formatter: BaseFormatter | None = None,
    ):
        super().__init__(min_level, formatter)

        if isinstance(token_or_bot, Bot):
            self.bot = token_or_bot
        else:
            if validate_token(token_or_bot):
                self.bot = Bot(token=token_or_bot)
            else:
                raise ValueError("not bot token")

        if isinstance(chat_id, int) or (
            chat_id.isdigit() or chat_id.isnumeric() or chat_id.isdecimal()
        ):
            self.chat_id = int(chat_id)
        else:
            raise ValueError("not chat id")

    async def emit(self, record: LogRecord) -> None:
        formatter = self.formatter or record.logger.get_formatter()
        await self.bot.send_message(self.chat_id, formatter.format(record))
