import re
from datetime import datetime

from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.types import ReplyKeyboardRemove

from back_end import send_post_request
from keyboard.kb_menu import languages
from keyboards import language_kb, phone_kb, skip_kb, phone_kb_ru, skip_kb_ru, main_menu_kb, main_menu_kb_ru
from middlewares import LanguageMiddleware
from state.register_state import Registration
from utils import validate_phone_number, convert_to_yyyy_mm_dd

router = Router()


@router.message(Command(commands=["start"]))
async def start_command(message: Message, state: FSMContext):
    await message.answer(
        "Tilni tanlang:\nВыберите язык:\n\n🇺🇿 O'zbek\n🇷🇺 Русский",
        reply_markup=language_kb
    )


@router.message(lambda msg: msg.text in languages)
async def choose_language(message: Message, state: FSMContext):
    lang = languages[message.text]
    LanguageMiddleware.set_language(message.from_user.id, lang)

    message_text = "Ismingizni kiriting:" if lang == 'uz' else "Введите ваше имя:"
    await message.answer(message_text, reply_markup=ReplyKeyboardRemove())
    await state.set_state(Registration.name)


@router.message(Registration.name)
async def ask_name(message: Message, state: FSMContext):
    lang = LanguageMiddleware.get_language(message.from_user.id)
    user_input = message.text.strip()

    if not re.match(r"^[A-Za-zА-Яа-яЎўҚқҒғҲҳШшЧчЁё\s\-]+$", user_input):
        if lang == "uz":
            await message.answer(
                "Ismingiz noto‘g‘ri kiritildi! Iltimos, faqat harflardan foydalanib ismingizni yozing."
            )
        elif lang == "ru":
            await message.answer("Ваше имя введено неверно! Пожалуйста, введите имя, используя только буквы.")
        return

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

        if not contact_number.startswith("+"):
            contact_number = "+" + contact_number
    else:
        contact_number = message.text.strip()

    validated_number = validate_phone_number(contact_number)

    if validated_number:
        await state.update_data(contact_number=validated_number)

        if lang == "uz":
            await message.answer("Tug'ilgan sanangizni kiriting yoki o'tkazib yuboring:", reply_markup=skip_kb)
        elif lang == "ru":
            await message.answer("Введите вашу дату рождения или пропустите:", reply_markup=skip_kb_ru)

        await state.set_state(Registration.birthday)
    else:
        if lang == "uz":
            await message.answer(
                "Telefon raqamingiz noto‘g‘ri formatda! "
                "Iltimos, raqamni quyidagi formatda kiriting: +998*********"
            )
        elif lang == "ru":
            await message.answer(
                "Номер телефона в неправильном формате! "
                "Пожалуйста, введите номер в следующем формате: +998*********"
            )


@router.message(Registration.birthday)
async def ask_birthdate(message: Message, state: FSMContext):
    lang = LanguageMiddleware.get_language(message.from_user.id)

    if message.text.lower() in ["❌ o'tkazib yuborish", "❌ пропустить"]:
        birthday = ""
    else:
        birthday = message.text
        if not re.match(r"^\d{2}-\d{2}-\d{4}$", birthday):
            if lang == "uz":
                await message.answer(
                    "Tug'ilgan sana noto'g'ri formatda! DD-MM-YYYY shaklida kiriting (masalan, DD-MM-YYYY):")
            elif lang == "ru":
                await message.answer(
                    "Дата рождения введена в неправильном формате! Введите в формате DD-MM-YYYY (например, DD-MM-YYYY):")
            return
        try:
            datetime.strptime(birthday, "%d-%m-%Y")
        except ValueError:
            if lang == "uz":
                await message.answer("Tug'ilgan sana noto'g'ri! DD-MM-YYYY formatida haqiqiy sana kiriting:")
            elif lang == "ru":
                await message.answer("Дата рождения неверна! Введите корректную дату в формате DD-MM-YYYY:")
            return

    await state.update_data(birthday=birthday)

    data = await state.get_data()

    try:
        data['birthday'] = convert_to_yyyy_mm_dd(data['birthday']) if data['birthday'] else ""
    except ValueError:
        pass

    data_profile = {
        "name": f"{data['name']}",
        "number": f"{data['contact_number']}",
        "birthday": f"{data['birthday']}",
        "tg_id": f"{message.from_user.id}"
    }

    response = send_post_request(data_profile)

    if response:
        if lang == "uz":
            await message.answer("Ro'yxatdan muvaffaqiyatli o'tdingiz!", reply_markup=main_menu_kb)
        elif lang == "ru":
            await message.answer("Вы успешно зарегистрированы!", reply_markup=main_menu_kb_ru)

    await state.clear()
