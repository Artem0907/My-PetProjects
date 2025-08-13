from aiogram import Router, F
from aiogram.filters import Command, CommandObject, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram_dialog import DialogManager

from start_menu.casino_dialog.casino_dialog_states import CasinoDialog

start_menu_router = Router()


@start_menu_router.message(Command('start'))
async def start_dialog_command(message: Message, state: FSMContext, dialog_manager: DialogManager):
    await dialog_manager.start(
        CasinoDialog.casino_main_menu,
        data={'balance': 100}
    )


@start_menu_router.message(F.text)
async def start_dialog_text(message: Message, state: FSMContext, dialog_manager: DialogManager):
    await dialog_manager.start(
        CasinoDialog.casino_main_menu,
        data={'balance': 100}
    )
