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
    phone = State()
    birthdate = State()


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
    await state.set_state(Registration.phone)


# Telefon raqamni so'rash
@router.message(Registration.phone)
async def ask_phone(message: Message, state: FSMContext):
    if message.contact:
        phone = message.contact.phone_number
    else:
        phone = message.text

    if len(phone) == 9 and phone.isdigit():
        await state.update_data(phone=phone)
        await message.answer("Tug'ilgan sanangizni kiriting yoki o'tkazib yuboring:", reply_markup=skip_kb)
        await state.set_state(Registration.birthdate)
    else:
        await message.answer("Telefon raqam noto'g'ri! Qaytadan kiriting:")


# Tug'ilgan sanani so'rash
@router.message(Registration.birthdate)
async def ask_birthdate(message: Message, state: FSMContext):
    if message.text.lower() == "❌ o'tkazib yuborish":
        birthdate = None
    else:
        birthdate = message.text

    await state.update_data(birthdate=birthdate)

    # Malumotlarni olish
    data = await state.get_data()
    data["tg_id"] = message.from_user.id
    await message.answer(f"Ro'yxatdan o'tdingiz!\n\n"
                         f"Ism: {data['name']}\n"
                         f"Telefon: {data['phone']}\n"
                         f"Tug'ilgan sana: {data.get('birthdate', "Ko'rsatilmagan")}")

    await state.clear()
    print(data)
