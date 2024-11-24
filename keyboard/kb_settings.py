from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Sozlamalar tugmalari
settings_kb_uz = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
settings_kb_uz.add(
    KeyboardButton("📞 Telefon raqamni o'zgartirish"),
    KeyboardButton("🌍 Tilni o'zgartirish"),
    KeyboardButton("✍️ Ismni o'zgartirish"),
    KeyboardButton("🎂 Tug'ilgan kunni qo'shish"),
    KeyboardButton("🔙 Orqaga")
)

settings_kb_ru = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
settings_kb_ru.add(
    KeyboardButton("📞 Изменить номер телефона"),
    KeyboardButton("🌍 Изменить язык"),
    KeyboardButton("✍️ Изменить имя"),
    KeyboardButton("🎂 Добавить дату рождения"),
    KeyboardButton("🔙 Назад")
)
