from aiogram import Bot
from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from config import ADMIN_ID
from middlewares import LanguageMiddleware
from state.feedback_state import FeedbackState

router = Router()


@router.message(lambda message: message.text in ["✍️ Izoh qoldirish", "✍️ Оставить отзыв"])
async def leave_feedback(message: Message, state: FSMContext):
    lang = LanguageMiddleware.get_language(message.from_user.id)
    if lang == "uz":
        await message.answer("Xizmatlarimiz yoki mahsulotlarimiz haqida izoh qoldiring:")
    elif lang == "ru":
        await message.answer("Оставьте отзыв о наших услугах или продуктах:")

    await state.set_state(FeedbackState.waiting_for_feedback)


@router.message(FeedbackState.waiting_for_feedback)
async def handle_feedback(message: Message, state: FSMContext, bot: Bot):
    user_feedback = message.text
    user_id = message.from_user.id
    lang = LanguageMiddleware.get_language(message.from_user.id)

    admin_message = f"📩 Yangi izoh:\n\n" \
                    f"🆔 Foydalanuvchi ID: {user_id}\n" \
                    f"✍️ Izoh: {user_feedback}"
    await bot.send_message(ADMIN_ID, admin_message)

    if lang == "uz":
        await message.answer("Izohingiz uchun rahmat!")
    elif lang == "ru":
        await message.answer("Спасибо за ваш отзыв!")

    await state.clear()
