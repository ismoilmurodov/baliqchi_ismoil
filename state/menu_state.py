from aiogram.fsm.state import StatesGroup, State


class RoomStateGroup(StatesGroup):
    cat = State()
    room = State()
