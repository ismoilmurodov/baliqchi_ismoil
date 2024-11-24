from aiogram import Router
from aiogram.types import Message
from middlewares import LanguageMiddleware
from keyboards.main import main_menu_kb_uz, main_menu_kb_ru

router = Router()

# "Xonalar haqida ma'lumot" ni bosganda
@router.message(text=["🏨 Xonalar haqida ma'lumot", "🏨 Информация о номерах"])
async def room_info(message: Message):
    lang = LanguageMiddleware.get_language(message.from_user.id)
    if lang == "uz":
        await message.answer("Xonalar haqida ma'lumot", reply_markup=main_menu_kb_uz)
    elif lang == "ru":
        await message.answer("Информация о номерах", reply_markup=main_menu_kb_ru)
