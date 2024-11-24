from aiogram import Router
from aiogram.types import Message, Location
from middlewares import LanguageMiddleware
from keyboard.kb_menu import location_kb_uz, location_kb_ru

router = Router()

# Menu tugmasini bosganda joylashuv tugmalarini ko'rsatish
@router.message(text=["📋 Menu", "📋 Меню"])
async def show_location_menu(message: Message):
    lang = LanguageMiddleware.get_language(message.from_user.id)
    if lang == "uz":
        await message.answer("Kerakli bo'limni tanlang:", reply_markup=location_kb_uz)
    elif lang == "ru":
        await message.answer("Выберите нужный раздел:", reply_markup=location_kb_ru)

# "Joylashuvlar ro'yxati" tugmasi uchun handler
@router.message(text=["📍 Joylashuvlar ro'yxati", "📍 Список местоположений"])
async def send_location_list(message: Message):
    lang = LanguageMiddleware.get_language(message.from_user.id)
    if lang == "uz":
        await message.answer("Joylashuvlar ro'yxati: kerakli manzilni tanlang.")
    elif lang == "ru":
        await message.answer("Список местоположений: выберите нужное место.")

# "Joylashuvni jo'natish" tugmasi uchun handler
@router.message(content_types=["location"])
async def confirm_location(message: Message):
    lang = LanguageMiddleware.get_language(message.from_user.id)
    user_location = message.location  # Foydalanuvchi joylashuvi
    print(f"Foydalanuvchi joylashuvi: {user_location.latitude}, {user_location.longitude}")
    if lang == "uz":
        await message.answer("Joylashuvingiz tasdiqlandi!")
    elif lang == "ru":
        await message.answer("Ваше местоположение подтверждено!")
