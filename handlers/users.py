import re

from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message
from aiogram.types import ReplyKeyboardRemove

from keyboards import language_kb, phone_kb, skip_kb, phone_kb_ru, skip_kb_ru
from middlewares import LanguageMiddleware

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
        "Tilni tanlang:\nВыберите язык:\n\n🇺🇿 O'zbek\n🇷🇺 Русский",
        reply_markup=language_kb
    )


@router.message(lambda msg: msg.text in languages)
async def choose_language(message: Message, state: FSMContext):
    lang = languages[message.text]
    LanguageMiddleware.set_language(message.from_user.id, lang)

    if lang == "uz":
        await message.answer("Ismingizni kiriting:", reply_markup=ReplyKeyboardRemove())
    elif lang == "ru":
        await message.answer("Введите ваше имя:", reply_markup=ReplyKeyboardRemove())

    await state.set_state(Registration.name)


@router.message(Registration.name)
async def ask_name(message: Message, state: FSMContext):
    lang = LanguageMiddleware.get_language(message.from_user.id)
    user_input = message.text.strip()

    # Tekshirish: Faqat harflar va bo'sh joyga ruxsat beriladi
    if not re.match(r"^[A-Za-zА-Яа-яЎўҚқҒғҲҳШшЧчЁё\s\-]+$", user_input):
        if lang == "uz":
            await message.answer(
                "Ismingiz noto‘g‘ri kiritildi! Iltimos, faqat harflardan foydalanib ismingizni yozing.")
        elif lang == "ru":
            await message.answer("Ваше имя введено неверно! Пожалуйста, введите имя, используя только буквы.")
        return  # To‘xtatib, foydalanuvchidan qayta kiritishni so‘raymiz.

    await state.update_data(name=message.text)
    if lang == "uz":
        await message.answer("Telefon raqamingizni ulashing yoki qo'lda kiriting:", reply_markup=phone_kb)
    elif lang == "ru":
        await message.answer("Поделитесь своим номером телефона или введите его вручную:", reply_markup=phone_kb_ru)

    await state.set_state(Registration.contact_number)


# Telefon raqamining to'g'ri formatini tekshirish
def validate_phone_number(contact_number):
    # 1. Agar foydalanuvchi '994' bilan boshlasa, uni '+998' formatiga o'zgartirish
    if contact_number.startswith("994") and not contact_number.startswith("+"):
        contact_number = "+998" + contact_number[3:]

    # 2. Raqamni +998 bilan boshlanishini va 9 ta raqamdan iboratligini tekshirish
    if re.match(r"^\+998\d{9}$", contact_number):
        return contact_number
    else:
        return None


@router.message(Registration.contact_number)
async def ask_phone(message: Message, state: FSMContext):
    lang = LanguageMiddleware.get_language(message.from_user.id)

    # 1. Kontakt yuborilganligini tekshirish
    if message.contact:
        # print(f"Yuborilgan kontakt: {message.contact.phone_number}")
        contact_number = message.contact.phone_number

        # Agar raqamda '+' bo'lmasa, qo'shamiz
        if not contact_number.startswith("+"):
            contact_number = "+" + contact_number
    else:
        contact_number = message.text.strip()
        print(f"Yuborilgan text: {contact_number}")

    # 2. Telefon raqamini tekshirish
    validated_number = validate_phone_number(contact_number)

    if validated_number:
        # Telefon raqami to'g'ri formatda bo'lsa
        await state.update_data(contact_number=validated_number)

        # Tug'ilgan sanani so'rash
        if lang == "uz":
            await message.answer("Tug'ilgan sanangizni kiriting yoki o'tkazib yuboring:", reply_markup=skip_kb)
        elif lang == "ru":
            await message.answer("Введите вашу дату рождения или пропустите:", reply_markup=skip_kb_ru)

        # Keyingi holatga o'tish
        await state.set_state(Registration.birthday)
    else:
        # Telefon raqami noto'g'ri formatda bo'lsa
        if lang == "uz":
            await message.answer(
                "Telefon raqamingiz noto‘g‘ri formatda! "
                "Iltimos, raqamni quyidagi formatda kiriting: +998901234567"
            )
        elif lang == "ru":
            await message.answer(
                "Номер телефона в неправильном формате! "
                "Пожалуйста, введите номер в следующем формате: +998901234567"
            )


from datetime import datetime
from back_end import send_post_request


# Sana formatini o'zgartirish funksiyasi
def convert_to_yyyy_mm_dd(date_str):
    try:
        date_object = datetime.strptime(date_str, "%d-%m-%Y")
        return date_object.strftime("%Y-%m-%d")  # 'YYYY-MM-DD' formatida qaytarish
    except ValueError:
        # Xato format haqida xabar berish
        raise ValueError(f"Invalid date format: {date_str}. Expected format is DD-MM-YYYY.")


@router.message(Registration.birthday)
async def ask_birthdate(message: Message, state: FSMContext):
    lang = LanguageMiddleware.get_language(message.from_user.id)

    if message.text.lower() in ["❌ o'tkazib yuborish", "❌ пропустить"]:
        birthday = ""  # Sana o‘tkazib yuborilgan
    else:
        birthday = message.text
        # Sana formatini tekshirish
        import re
        if not re.match(r"^\d{2}-\d{2}-\d{4}$", birthday):
            if lang == "uz":
                await message.answer(
                    "Tug'ilgan sana noto'g'ri formatda! DD-MM-YYYY shaklida kiriting (masalan, 11-08-2003):")
            elif lang == "ru":
                await message.answer(
                    "Дата рождения введена в неправильном формате! Введите в формате DD-MM-YYYY (например, 11-08-2003):")
            return
        try:
            datetime.strptime(birthday, "%d-%m-%Y")
        except ValueError:
            if lang == "uz":
                await message.answer("Tug'ilgan sana noto'g'ri! DD-MM-YYYY formatida haqiqiy sana kiriting:")
            elif lang == "ru":
                await message.answer("Дата рождения неверна! Введите корректную дату в формате DD-MM-YYYY:")
            return

    # Davlatga ma'lumotni saqlash
    await state.update_data(birthday=birthday)

    # Foydalanuvchi ma'lumotlarini olish
    data = await state.get_data()

    # Sana formatini o'zgartirish
    try:
        data['birthday'] = convert_to_yyyy_mm_dd(data['birthday']) if data['birthday'] else ""
    except ValueError as e:
        await message.answer(str(e))
        return

    # Foydalanuvchi ma'lumotlarini yig'ish
    data_profile = {
        "username": f"{data['name']}",
        "contact_number": f"{data['contact_number']}",
        "birthday": f"{data['birthday']}",
        "user_tg_id": f"{message.from_user.id}"
    }
    print(data_profile)  # Ma'lumotlarni tekshirish uchun

    # Tashqi API'ga ma'lumotlarni yuborish
    response = send_post_request(data_profile)

    if response:
        if lang == "uz":
            await message.answer("Ro'yxatdan muvaffaqiyatli o'tdingiz!")
        elif lang == "ru":
            await message.answer("Вы успешно зарегистрированы!")
        print(f"Status Code: {response.status_code}")
        print(f"Response Body: {response.text}")

    # await message.answer(data_profile)
    await state.clear()
    # print(data)  # Admin uchun

# @router.message(Registration.birthday)
# async def ask_birthdate(message: Message, state: FSMContext):
#     lang = LanguageMiddleware.get_language(message.from_user.id)
#
#     if message.text.lower() in ["❌ o'tkazib yuborish", "❌ пропустить"]:
#         birthday = None
#     else:
#         birthday = message.text
#
#     await state.update_data(birthday=birthday)
#
#     data = await state.get_data()
#     data["tg_id"] = message.from_user.id
#
#     from datetime import datetime
#
#     def convert_to_yyyy_mm_dd(date_str):
#
#         try:
#
#             date_object = datetime.strptime(date_str, "%d-%m-%Y")
#
#             # Format the date to 'YYYY-MM-DD'
#             return date_object.strftime("%Y-%m-%d")
#
#         except ValueError:
#             # Handle invalid format or parsing error
#             raise ValueError(f"Invalid date format: {date_str}. Expected format is YYYY-MM-DD.")
#     data['birthday'] = convert_to_yyyy_mm_dd(data['birthday'])
#
#     data_profile = {
#         "username": f"{data['name']}",
#         "contact_number": f"{data['contact_number']}",
#         "birthday": f"{data['birthday']}",
#         "user_tg_id": f"{data['tg_id']}"
#     }
#     print(data_profile)
#     from back_end import send_post_request
#     response = send_post_request(data_profile)
#
#     if response:
#         print(f"Status Code: {response.status_code}")
#         print(f"Response Body: {response.text}")
#
#     if lang == "uz":
#         success_message = (
#             f"Ro'yxatdan o'tdingiz!\n\n"
#             f"Ism: {data['name']}\n"
#             f"Telefon: {data['contact_number']}\n"
#             f"Tug'ilgan sana: {data.get('birthday', "Ko'rsatilmagan")}"
#         )
#     elif lang == "ru":
#         success_message = (
#             f"Вы зарегистрированы!\n\n"
#             f"Имя: {data['name']}\n"
#             f"Телефон: {data['contact_number']}\n"
#             f"Дата рождения: {data.get('birthday', 'Не указано')}"
#         )

# await message.answer(success_message)
# await state.clear()
# print(data)  # Admin uchun
