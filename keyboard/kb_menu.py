from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# O'zbek tilidagi tugmalar (Uzbek language buttons)
location_kb_uz = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="📍 Joylashuvlar ro'yxati", ),  # Locations list
            KeyboardButton(text="📍 Joylashuvni yuborish", )  # Send location
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

# Botning barcha tillari
languages = {"🇺🇿 O'zbek": "uz", "🇷🇺 Русский": "ru"}
