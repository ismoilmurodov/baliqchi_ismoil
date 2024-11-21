from aiogram.types import ReplyKeyboardMarkup, KeyboardButton,ReplyKeyboardRemove

# Tilni tanlash uchun klaviatura
language_kb = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="🇺🇿 O'zbek")],
    [KeyboardButton(text="🇷🇺 Русский")]
], resize_keyboard=True,ReplyKeyboardRemove=True)

# Telefon raqamini ulashish uchun klaviatura
phone_kb = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="📱 Telefon raqamni ulashish", request_contact=True)]
], resize_keyboard=True, one_time_keyboard=True)

# O'tkazib yuborish tugmasi uchun klaviatura
skip_kb = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="❌ O'tkazib yuborish")]
], resize_keyboard=True)
