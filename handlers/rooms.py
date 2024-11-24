from aiogram import Router
from aiogram.types import Message

from middlewares import LanguageMiddleware

router = Router()


@router.message(lambda message: message.text in ["🏨 Xonalar haqida ma'lumot", "🏨 Информация о номерах"])
async def room_info(message: Message):
    lang = LanguageMiddleware.get_language(message.from_user.id)

    if lang == "uz":
        await message.answer("Xonalar haqida ma'lumot")
    elif lang == "ru":
        await message.answer("Информация о номерах")
