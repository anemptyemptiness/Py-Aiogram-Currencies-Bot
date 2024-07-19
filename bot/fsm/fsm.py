from aiogram.fsm.state import State, StatesGroup


class StartSG(StatesGroup):
    menu = State()


class ExchangeSG(StatesGroup):
    exchange = State()


class RatesSG(StatesGroup):
    rates = State()
    rate = State()
