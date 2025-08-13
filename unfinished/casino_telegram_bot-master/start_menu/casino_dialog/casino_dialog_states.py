from aiogram.fsm.state import StatesGroup, State


class CasinoDialog(StatesGroup):
    casino_main_menu = State()
    roulette = State()
    roulette_choose_bet = State()
    roulette_set_bet = State()
