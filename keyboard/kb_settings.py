from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Sozlamalar tugmalari - Uzbek version
settings_kb_uz = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [KeyboardButton(text="📞 Telefon raqamni o'zgartirish")],
        [KeyboardButton(text="🌍 Tilni o'zgartirish")],
        [KeyboardButton(text="✍️ Ismni o'zgartirish")],
        [KeyboardButton(text="🎂 Tug'ilgan kunni qo'shish")],
        [KeyboardButton(text="🔙 Orqaga")]
    ]
)

# Sozlamalar tugmalari - Russian version
settings_kb_ru = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [KeyboardButton(text="📞 Изменить номер телефона")],
        [KeyboardButton(text="🌍 Изменить язык")],
        [KeyboardButton(text="✍️ Изменить имя")],
        [KeyboardButton(text="🎂 Добавить дату рождения")],
        [KeyboardButton(text="🔙 Назад")]
    ]
)
