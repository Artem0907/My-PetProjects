from aiogram import Router
from start_menu.casino_dialog.casino_dialog import casino_dialog

casino_dialog_router = Router()

casino_dialog_router.include_router(casino_dialog)
