from aiogram import Router, types
from aiogram.types import Message
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from keyboards import language_kb, phone_kb, skip_kb
from middlewares import LanguageMiddleware

from aiogram import Router
from aiogram import types
from aiogram.filters import Command
from aiogram.types import Message

router = Router()

# Botning barcha tillari
languages = {"🇺🇿 O'zbek": "uz", "🇷🇺 Русский": "ru"}


# Holatlarni yaratish
class Registration(StatesGroup):
    name = State()
    contact_number = State()
    birthday = State()


# /start komandasini qayta ishlash
# @router.message(CommandStart("/start"))
@router.message(Command(commands=["start"]))
async def start_command(message: Message, state: FSMContext):
    await message.answer("Salom! Tilni tanlang:", reply_markup=language_kb)


# Tilni tanlash
@router.message(lambda msg: msg.text in languages)
async def choose_language(message: Message, state: FSMContext):
    lang = languages[message.text]
    LanguageMiddleware.set_language(message.from_user.id, lang)
    await message.answer("Ismingizni kiriting:")
    await state.set_state(Registration.name)


# Ismni so'rash
@router.message(Registration.name)
async def ask_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Telefon raqamingizni ulashing yoki qo'lda kiriting:", reply_markup=phone_kb)
    await state.set_state(Registration.contact_number)


@router.message(Registration.contact_number)
async def ask_phone(message: Message, state: FSMContext):
    # Agar foydalanuvchi tugma orqali ulashsa
    if message.contact:
        contact_number = message.contact.phone_number
    else:
        contact_number = message.text

    # Telefon raqamni tekshirish
    if contact_number.startswith("+998") and len(contact_number[4:]) == 9 and contact_number[4:].isdigit():
        await state.update_data(contact_number=contact_number)
        await message.answer("Tug'ilgan sanangizni kiriting yoki o'tkazib yuboring:", reply_markup=skip_kb)
        await state.set_state(Registration.birthday)
    else:
        await message.answer(
            "Telefon raqam noto'g'ri formatda! "
            "Raqamni quyidagi formatda kiriting: +998901234567"
        )


# Tug'ilgan sanani so'rash
@router.message(Registration.birthday)
async def ask_birthdate(message: Message, state: FSMContext):
    if message.text.lower() == "❌ o'tkazib yuborish":
        birthday = None
    else:
        birthday = message.text

    await state.update_data(birthday=birthday)

    # Malumotlarni olish
    data = await state.get_data()
    data["tg_id"] = message.from_user.id
    await message.answer(f"Ro'yxatdan o'tdingiz!\n\n"
                         f"Ism: {data['name']}\n"
                         f"Telefon: {data['contact_number']}\n"
                         f"Tug'ilgan sana: {data.get('birthday', "Ko'rsatilmagan")}")

    await state.clear()
    print(data)
