from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# O'zbek tilidagi tugmalar
location_kb_uz = ReplyKeyboardMarkup(resize_keyboard=True)
location_kb_uz.add(
    KeyboardButton("📍 Joylashuvlar ro'yxati"),
    KeyboardButton("📍 Joylashuvni jo'natish", request_location=True)
)

# Rus tilidagi tugmalar
location_kb_ru = ReplyKeyboardMarkup(resize_keyboard=True)
location_kb_ru.add(
    KeyboardButton("📍 Список местоположений"),
    KeyboardButton("📍 Отправить местоположение", request_location=True)
)


# # O'zbek va Rus tillaridagi tugmalar allaqachon mavjud
# main_menu_kb_uz.add(KeyboardButton("✍️ Izoh qoldirish"))
# main_menu_kb_ru.add(KeyboardButton("✍️ Оставить отзыв"))
