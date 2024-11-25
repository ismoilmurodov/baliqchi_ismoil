from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# O'zbek tilidagi tugmalar (Uzbek language buttons)
location_kb_uz = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="📍 Joylashuvlar ro'yxati"),  # Locations list
            KeyboardButton(text="📍 Joylashuvni yuborish", request_location=True),  # Send location button
        ],
        [
            KeyboardButton(text="⬅️ Qaytish")  # Back button
        ]
    ],
    resize_keyboard=True  # Resize the keyboard for better user experience
)

# Rus tilidagi tugmalar (Russian language buttons)
location_kb_ru = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="📍 Список местоположений"),  # Locations list
            KeyboardButton(text="📍 Отправить местоположение", request_location=True), ],

        [KeyboardButton(text="⬅️ Назад")]  # Send location
    ],
    resize_keyboard=True
)

# Botning barcha tillari
languages = {"🇺🇿 O'zbek": "uz", "🇷🇺 Русский": "ru"}
