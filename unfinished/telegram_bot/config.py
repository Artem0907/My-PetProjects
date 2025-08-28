from dotenv import load_dotenv
from os import getenv
from asyncio import get_event_loop

from bot_types.bot import BotData


load_dotenv()

bot_token = getenv("BOT_TOKEN")
if not bot_token:
    raise ValueError("Invalid bot token")

async_run = get_event_loop().run_until_complete
bot_data = BotData(bot_token)
