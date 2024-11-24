from aiogram import Bot
from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message

from middlewares import LanguageMiddleware

router = Router()


# Izoh holatini saqlash uchun
class FeedbackState(StatesGroup):
    waiting_for_feedback = State()


ADMIN_ID = "123456789"  # Adminning Telegram ID'sini bu yerga kiriting


# "Izoh qoldirish" tugmasi bosilganda handler
@router.message(lambda message: message.text in ["✍️ Izoh qoldirish", "✍️ Оставить отзыв"])
async def leave_feedback(message: Message, state: FSMContext):
    lang = LanguageMiddleware.get_language(message.from_user.id)
    if lang == "uz":
        await message.answer("Xizmatlarimiz yoki mahsulotlarimiz haqida izoh qoldiring:")
    elif lang == "ru":
        await message.answer("Оставьте отзыв о наших услугах или продуктах:")

    # Set the state to "waiting_for_feedback"
    await state.set_state(FeedbackState.waiting_for_feedback)


# Foydalanuvchi izoh yuborganida
@router.message(FeedbackState.waiting_for_feedback)
async def handle_feedback(message: Message, state: FSMContext, bot: Bot):
    user_feedback = message.text
    user_id = message.from_user.id
    lang = LanguageMiddleware.get_language(message.from_user.id)

    # Adminga izohni jo'natish
    admin_message = f"📩 Yangi izoh:\n\n" \
                    f"🆔 Foydalanuvchi ID: {user_id}\n" \
                    f"✍️ Izoh: {user_feedback}"
    await bot.send_message(ADMIN_ID, admin_message)

    # Foydalanuvchiga javob qaytarish
    if lang == "uz":
        await message.answer("Izohingiz uchun rahmat!")
    elif lang == "ru":
        await message.answer("Спасибо за ваш отзыв!")

    # Holatni tozalash
    await state.clear()  # Holatni tozalash
