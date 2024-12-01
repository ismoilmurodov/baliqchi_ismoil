from aiogram.fsm.state import StatesGroup, State


class OrderState(StatesGroup):
    category = State()
    product = State()
    product_quantity = State()  # To store the product quantity
    cart = State()  # To store the cart's items
    back = State()


class OrderProcess(StatesGroup):
    order_type = State()

