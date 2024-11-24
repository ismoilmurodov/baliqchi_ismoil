from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Tilni tanlash uchun klaviatura
language_kb = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="🇺🇿 O'zbek")],
    [KeyboardButton(text="🇷🇺 Русский")]
], resize_keyboard=True, ReplyKeyboardRemove=True)

phone_kb = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="📱 Telefon raqamni ulashish", request_contact=True)]
], resize_keyboard=True, one_time_keyboard=True)

phone_kb_ru = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="📱 Поделитесь своим номером телефона", request_contact=True)]
], resize_keyboard=True, one_time_keyboard=True)

# O'tkazib yuborish tugmasi uchun klaviatura
skip_kb = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="❌ O'tkazib yuborish")]
], resize_keyboard=True, input_field_placeholder="DD-MM-YYYY")

# O'tkazib yuborish tugmasi uchun klaviatura (ru)
skip_kb_ru = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="❌ Пропустить")]
], resize_keyboard=True, input_field_placeholder="DD-MM-YYYY")

# Asosiy menu tugmalari (O'zbek tilida)
main_menu_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="📋 Menu"),
            KeyboardButton(text="🛍 Buyurtmalar tarixi"),
        ],
        [
            KeyboardButton(text="✍️ Izoh qoldirish"),
            KeyboardButton(text="⚙️ Sozlamalar"),
        ],
        [
            KeyboardButton(text="🏨 Xonalar haqida ma'lumot"),
        ],
    ],
    resize_keyboard=True
)

# Asosiy menu tugmalari (Rus tilida)
main_menu_kb_ru = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="📋 Меню"),
            KeyboardButton(text="🛍 История заказов"),
        ],
        [
            KeyboardButton(text="✍️ Оставить отзыв"),
            KeyboardButton(text="⚙️ Настройки"),
        ],
        [
            KeyboardButton(text="🏨 Информация о номерах"),
        ],
    ],
    resize_keyboard=True
)
