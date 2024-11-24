from aiogram.fsm.state import StatesGroup, State


class Registration(StatesGroup):
    name = State()
    contact_number = State()
    birthday = State()
