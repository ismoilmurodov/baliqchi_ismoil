from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# O'zbek tilidagi tugmalar (Uzbek language buttons)
location_kb_uz = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="📍 Joylashuvlar ro'yxati", ),  # Locations list
            KeyboardButton(text="📍 Joylashuvni jo'natish", )  # Send location
        ]
    ],
    resize_keyboard=True
)

# Rus tilidagi tugmalar (Russian language buttons)
location_kb_ru = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="📍 Список местоположений"),  # Locations list
            KeyboardButton(text="📍 Отправить местоположение", )  # Send location
        ]
    ],
    resize_keyboard=True
)

# Example for adding additional buttons (like feedback) to the main menu:
# main_menu_kb_uz = ReplyKeyboardMarkup(
#     keyboard=[
#         [KeyboardButton("✍️ Izoh qoldirish")]  # Leave a comment
#     ],
#     resize_keyboard=True
# )

# main_menu_kb_ru = ReplyKeyboardMarkup(
#     keyboard=[
#         [KeyboardButton("✍️ Оставить отзыв")]  # Leave a review
#     ],
#     resize_keyboard=True
# )
