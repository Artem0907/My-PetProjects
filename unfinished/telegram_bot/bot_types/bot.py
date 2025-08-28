from typing import NoReturn
from aiogram import Bot
from aiogram.exceptions import TelegramUnauthorizedError
from asyncio import get_event_loop


class BotData:
    def __init__(self, token: str) -> NoReturn | None:
        if len(token.split(":")) == 2 and token.split(":")[0].isdigit():
            try:
                self.token = token
                self.bot = Bot(token)
                get_event_loop().run_until_complete(self.bot.get_me())
            except TelegramUnauthorizedError:
                raise ValueError("Invalid bot token (bot not registered)")
        else:
            raise ValueError("Invalid bot token")

    def __repr__(self) -> str:
        return f"BotToken({self.token})"
