from asyncio import run as aio_run

from aiogram import Bot, Dispatcher, F, Router
from aiogram.client.default import DefaultBotProperties
from aiogram.filters.command import Command
from aiogram.types import Message
from nest_asyncio import (  # type: ignore[import-untyped]
    apply as asyncio_loop_apply,
)
from tortoise import Tortoise

from .models import UserCommands, UserMessages
from .settings import get_settings
from .turbo_print.logger import TurboLogger

router = Router()
settings = get_settings()


async def set_database() -> Tortoise:
    database = Tortoise()
    await database.init(
        db_url=settings.database.url,
        modules={"models": ["src.models"]},
        use_tz=False,
        timezone=settings.timezone,
    )
    await database.generate_schemas(True)
    await Tortoise.get_connection("default").execute_query("SELECT 1")
    return database


@router.message(Command("start"))
async def command_start(message: Message) -> None:
    user_id = message.from_user.id if message.from_user else 0
    await UserCommands.create(
        message_id=message.message_id,
        chat_id=message.chat.id,
        user_id=user_id,
        command="start",
    )
    await message.answer("hello user")


@router.message(Command("id"))
async def get_user_id(message: Message) -> None:
    user_id = message.from_user.id if message.from_user else 0
    await UserCommands.create(
        message_id=message.message_id,
        chat_id=message.chat.id,
        user_id=user_id,
        command="id",
    )
    await message.reply(
        f"your id: <code>{message.from_user.id}</code>"
        if message.from_user
        else "sorry, your not user"
    )


@router.message(Command("is_admin"))
async def user_is_admin_command(message: Message) -> None:
    user_id = message.from_user.id if message.from_user else None
    await UserCommands.create(
        message_id=message.message_id,
        chat_id=message.chat.id,
        user_id=user_id or 0,
        command="is_admin",
    )
    if not user_id:
        message.answer("you not user, sorry")

    if user_id and user_id == settings.bot.creator:
        await message.answer("you creator")
    elif user_id and user_id in settings.bot.admins:
        await message.answer("you admin")
    else:
        await message.answer("you user")


@router.message(F.text)
async def echo_command(message: Message) -> None:
    user_id = message.from_user.id if message.from_user else 0
    await UserMessages.create(
        message_id=message.message_id,
        chat_id=message.chat.id,
        user_id=user_id,
        message=message.text or "",
    )
    await message.reply(message.text or "")


async def start() -> None:

    bot = Bot(
        settings.bot.token,
        default=DefaultBotProperties(parse_mode=settings.bot.parse_mode),
    )
    dp = Dispatcher()
    db = await set_database()  # noqa: F841
    logger = TurboLogger.get_logger("bot")

    dp.include_routers(router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    try:
        asyncio_loop_apply()
        aio_run(start())
    except KeyboardInterrupt:
        exit(0)
