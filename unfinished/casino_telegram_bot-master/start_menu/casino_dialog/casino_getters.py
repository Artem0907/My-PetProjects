from pprint import pprint

from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import ManagedCounter


async def first_window_start_data(dialog_manager: DialogManager, **_kwargs):
    return dialog_manager.start_data


async def bet_getter(dialog_manager: ManagedCounter, **kwargs):
    bet_counter: ManagedCounter = dialog_manager.find('roulette_bet_counter')
    bet = bet_counter.get_value()
    balance = dialog_manager.start_data['balance']
    coefficient = dialog_manager.dialog_data['coefficient']

    potential_gain = bet * coefficient

    if bet == balance:
        return None
    else:
        return {
            'balance': balance,
            'bet': bet,
            'potential_gain': potential_gain
        }

