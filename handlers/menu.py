from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from keyboard.kb_menu import location_kb_uz, location_kb_ru
from middlewares import LanguageMiddleware

router = Router()


# Menu tugmasini bosganda joylashuv tugmalarini ko'rsatish
@router.message(lambda message: message.text in ["📋 Menu", "📋 Меню"])
async def show_location_menu(message: Message, state: FSMContext):
    # Retrieve the user's language from your language middleware
    lang = LanguageMiddleware.get_language(message.from_user.id)

    # Send the appropriate response based on language
    if lang == "uz":
        await message.answer("Kerakli bo'limni tanlang:", reply_markup=location_kb_uz)
    elif lang == "ru":
        await message.answer("Выберите нужный раздел:", reply_markup=location_kb_ru)
    else:
        # Default case if the language is not recognized
        await message.answer("Please select the necessary section:", reply_markup=location_kb_uz)




# "Joylashuvlar ro'yxati" tugmasi uchun handler
@router.message(lambda message: message.text in ["📍 Joylashuvlar ro'yxati", "📍 Список местоположений"])
async def send_location_list(message: Message, state: FSMContext):
    lang = LanguageMiddleware.get_language(message.from_user.id)
    if lang == "uz":
        await message.answer("Joylashuvlar ro'yxati: kerakli manzilni tanlang.")
    elif lang == "ru":
        await message.answer("Список местоположений: выберите нужное место.")


# "Joylashuvni jo'natish" tugmasi uchun handler
@router.message(lambda message: message.location is not None)
async def confirm_location(message: Message, state: FSMContext):
    lang = LanguageMiddleware.get_language(message.from_user.id)
    user_location = message.location  # Foydalanuvchi joylashuvi
    print(f"Foydalanuvchi joylashuvi: {user_location.latitude}, {user_location.longitude}")
    if lang == "uz":
        await message.answer("Joylashuvingiz tasdiqlandi!")
    elif lang == "ru":
        await message.answer("Ваше местоположение подтверждено!")
