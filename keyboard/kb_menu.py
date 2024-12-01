from aiogram.fsm.state import StatesGroup, State
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

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


def create_default_keyboard(kb_buttons_list):
    keyboard = ReplyKeyboardBuilder()
    for kb_button in kb_buttons_list:
        keyboard.add(KeyboardButton(text=kb_button))
    return keyboard.adjust(1, repeat=True).as_markup(resize_keyboard=True)
