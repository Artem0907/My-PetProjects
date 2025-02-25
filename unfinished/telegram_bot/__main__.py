from bot_types.bot import BotData
from config import bot_data, async_run


async def start_bot(bot_data: BotData): ...


if __name__ == "__main__":
    try:
        async_run(start_bot(bot_data))
    except KeyboardInterrupt:
        pass
    finally:
        async_run(bot_data.bot.session.close())
