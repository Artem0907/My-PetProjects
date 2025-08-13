import asyncio

from aiogram import Bot, Dispatcher
from aiogram.types import ErrorEvent
from aiogram_dialog import setup_dialogs, DialogManager
from aiogram_dialog.api.exceptions import UnknownIntent, OutdatedIntent

from settings import bot_token
from start_menu.casino_dialog.casino_dialog_router import casino_dialog_router
from start_menu.start_menu_router import start_menu_router


async def bot_start():
    # main configuration
    bot = Bot(token=bot_token)
    dp = Dispatcher()
    setup_dialogs(dp)

    async def error_unknown_intent_handler(
            event: ErrorEvent, dialog_manager: DialogManager
    ):
        if isinstance(event.exception, UnknownIntent) or isinstance(event.exception, OutdatedIntent):
            try:
                event_message_id = event.update.callback_query.message.message_id
                event_chat_id = event.update.callback_query.message.chat.id
                await bot.delete_message(
                    chat_id=event_chat_id, message_id=event_message_id
                )
            except AttributeError:
                print(f'Отбилась в закрытый диалог.')
            except Exception as exception:
                print(exception)

        else:
            return print(f"{event}")

    # error handler
    dp.errors.register(error_unknown_intent_handler)

    # handlers routers
    dp.include_router(start_menu_router)

    # dialog routers
    dp.include_router(casino_dialog_router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(bot_start())
    except Exception as e:
        print(e)
