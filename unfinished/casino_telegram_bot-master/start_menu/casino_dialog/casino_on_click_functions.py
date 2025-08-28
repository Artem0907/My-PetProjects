from pprint import pprint

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button, ManagedCounter

from start_menu.casino_dialog.casino_data import BET_TYPES
from start_menu.casino_dialog.casino_dialog_states import CasinoDialog


async def close_dialog(
        callback: CallbackQuery, button: Button, dialog_manager: DialogManager
):
    try:
        await dialog_manager.done()
    except Exception as e:
        print(e)
        pass


async def choose_set(
        callback: CallbackQuery, button: Button, dialog_manager: DialogManager
):
    bet_id = callback.data
    bet_info = BET_TYPES.get(bet_id)

    if not bet_info:
        await callback.answer("Ошибка выбора ставки", show_alert=True)
        return

    dialog_manager.dialog_data['title'] = bet_info.get('title')
    dialog_manager.dialog_data['coefficient'] = bet_info.get('coefficient')

    await dialog_manager.switch_to(
        CasinoDialog.roulette_set_bet
    )



async def set_bet_click(
        event: CallbackQuery,
        widget: ManagedCounter,
        dialog_manager: DialogManager,
) -> None:
    await event.answer(f"Value: {widget.get_value()}")


async def on_bet_changed(
        event: CallbackQuery,
        widget: ManagedCounter,
        dialog_manager: DialogManager,
) -> None:
    current_value = widget.get_value()
    current_balance = dialog_manager.start_data['balance']

    print(current_value)
    print(current_balance)

    if current_balance == current_value:
        await event.answer(
            'stop'
        )
        return