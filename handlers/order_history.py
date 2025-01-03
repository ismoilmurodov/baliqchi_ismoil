from aiogram import Router
from aiogram.types import Message

from middlewares import LanguageMiddleware

router = Router()


@router.message(lambda message: message.text in ["🛍 Buyurtmalar tarixi", "🛍 История заказов"])
async def show_orders_history(message: Message):
    lang = LanguageMiddleware.get_language(message.from_user.id)
    if lang == "uz":
        await message.answer("Sizning buyurtmalaringiz:")
    elif lang == "ru":
        await message.answer("Ваши заказы:")
