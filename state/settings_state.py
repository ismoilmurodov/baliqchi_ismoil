from aiogram.fsm.state import StatesGroup, State


class SettingsState(StatesGroup):
    phone_change = State()
    language_change = State()
    name_change = State()
    birthday_change = State()
