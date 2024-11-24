from aiogram.fsm.state import StatesGroup, State


class FeedbackState(StatesGroup):
    waiting_for_feedback = State()
