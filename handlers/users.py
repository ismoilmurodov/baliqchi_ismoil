from aiogram import Router, types
from aiogram.types import Message
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from keyboards import language_kb, phone_kb, skip_kb,phone_kb_ru,skip_kb_ru
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
    await message.answer(
        "Выберите язык:\n\n🇺🇿 O'zbek\n🇷🇺 Русский",
        reply_markup=language_kb
    )


@router.message(lambda msg: msg.text in languages)
async def choose_language(message: Message, state: FSMContext):
    lang = languages[message.text]
    LanguageMiddleware.set_language(message.from_user.id, lang)

    if lang == "uz":
        await message.answer("Ismingizni kiriting:")
    elif lang == "ru":
        await message.answer("Введите ваше имя:")

    await state.set_state(Registration.name)


@router.message(Registration.name)
async def ask_name(message: Message, state: FSMContext):
    lang = LanguageMiddleware.get_language(message.from_user.id)

    await state.update_data(name=message.text)
    if lang == "uz":
        await message.answer("Telefon raqamingizni ulashing yoki qo'lda kiriting:", reply_markup=phone_kb)
    elif lang == "ru":
        await message.answer("Поделитесь своим номером телефона или введите его вручную:", reply_markup=phone_kb_ru)

    await state.set_state(Registration.contact_number)


@router.message(Registration.contact_number)
async def ask_phone(message: Message, state: FSMContext):
    lang = LanguageMiddleware.get_language(message.from_user.id)

    if message.contact:
        contact_number = message.contact.phone_number
    else:
        contact_number = message.text

    if contact_number.startswith("+998") and len(contact_number[4:]) == 9 and contact_number[4:].isdigit():
        await state.update_data(contact_number=contact_number)
        if lang == "uz":
            await message.answer("Tug'ilgan sanangizni kiriting yoki o'tkazib yuboring:", reply_markup=skip_kb)
        elif lang == "ru":
            await message.answer("Введите вашу дату рождения или пропустите:", reply_markup=skip_kb_ru)
        await state.set_state(Registration.birthday)
    else:
        if lang == "uz":
            await message.answer(
                "Telefon raqam noto'g'ri formatda! "
                "Raqamni quyidagi formatda kiriting: +998901234567"
            )
        elif lang == "ru":
            await message.answer(
                "Номер телефона в неправильном формате! "
                "Введите номер в следующем формате: +998901234567"
            )


@router.message(Registration.birthday)
async def ask_birthdate(message: Message, state: FSMContext):
    lang = LanguageMiddleware.get_language(message.from_user.id)

    if message.text.lower() in ["❌ o'tkazib yuborish", "❌ пропустить"]:
        birthday = None
    else:
        birthday = message.text

    await state.update_data(birthdate=birthday)

    data = await state.get_data()
    data["tg_id"] = message.from_user.id

    if lang == "uz":
        success_message = (
            f"Ro'yxatdan o'tdingiz!\n\n"
            f"Ism: {data['name']}\n"
            f"Telefon: {data['contact_number']}\n"
            f"Tug'ilgan sana: {data.get('birthday', "Ko'rsatilmagan")}"
        )
    elif lang == "ru":
        success_message = (
            f"Вы зарегистрированы!\n\n"
            f"Имя: {data['name']}\n"
            f"Телефон: {data['contact_number']}\n"
            f"Дата рождения: {data.get('birthday', 'Не указано')}"
        )

    await message.answer(success_message)
    await state.clear()
    print(data)  # Admin uchun

