from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def generate_cart_keyboard(products):
    keyboard = [
        [
            InlineKeyboardButton(text="Оформить заказ", callback_data='order'),
            InlineKeyboardButton(text="Очистить корзинку", callback_data='clear_cart')
        ]
    ]

    # Add each product with a button to delete it
    for product in products:
        keyboard.append([InlineKeyboardButton(text=product, callback_data=f"delete_{product}")])

    return InlineKeyboardMarkup(inline_keyboard=keyboard)


# Клавиатура для подтверждения заказа
def generate_confirmation_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="✅ Подтвердить")],
            [KeyboardButton(text="❌ Отменить")],
        ],  # Кнопки упакованы в список
        resize_keyboard=True  # Настройка размера
    )
    return keyboard


def order_message(total_price, delivery_price, order_products):
    # Формируем сообщение для пользователя
    message_text = f"""
🛒 В корзине:
{order_products}

💰 Товары: {total_price} сум
🚚 Доставка: {delivery_price} сум
🏷️ Итого: {total_price + delivery_price} сум
"""
    return message_text


# Клавиатура для выбора типа оплаты
def generate_payment_keyboard():
    # Создаём кнопки
    buttons = [
        [KeyboardButton(text="💳 Карта")],
        [KeyboardButton(text="💸 Payme")],
        [KeyboardButton(text="📱 Click")],
        [KeyboardButton(text="⬅️ Назад")]  # кнопка назад
    ]

    # Создаём клавиатуру с обязательным параметром type
    keyboard = ReplyKeyboardMarkup(
        keyboard=buttons,  # Передаем список кнопок
        resize_keyboard=True  # Указываем resize
    )

    return keyboard


# Helper function to create inline keyboard
def create_inline_keyboard(product_name, quantity):
    button_decrease = InlineKeyboardButton(
        text="➖", callback_data=f"quantity_decrease_{product_name}")
    button_quantity = InlineKeyboardButton(
        text=str(quantity), callback_data="quantity_current")
    button_increase = InlineKeyboardButton(
        text="➕", callback_data=f"quantity_increase_{product_name}")
    button_add_to_cart = InlineKeyboardButton(
        text="🛒 Добавить в корзинку", callback_data=f"add_to_cart_{product_name}")

    return InlineKeyboardMarkup(row_width=3, inline_keyboard=[
        [button_decrease, button_quantity, button_increase],
        [button_add_to_cart]
    ])
