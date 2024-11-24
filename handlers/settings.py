from aiogram import Router
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State
from aiogram.fsm import StateGroup

from handlers.feedback import ADMIN_ID
from middlewares import LanguageMiddleware
from keyboard.kb_settings import settings_kb_uz, settings_kb_ru

router = Router()


# Sozlamalar uchun holatlar
class SettingsState(StateGroup):
    phone_change = State()  # Telefon raqami o'zgartirish
    language_change = State()  # Til o'zgartirish
    name_change = State()  # Ism o'zgartirish
    birthday_change = State()  # Tug'ilgan kun o'zgartirish


# "Sozlamalar" tugmasi bosilganda
@router.message(text=["⚙️ Sozlamalar", "⚙️ Настройки"])
async def settings_menu(message: Message):
    lang = LanguageMiddleware.get_language(message.from_user.id)
    if lang == "uz":
        await message.answer("Quyidagi sozlamalarni o'zgartirishingiz mumkin:", reply_markup=settings_kb_uz)
    elif lang == "ru":
        await message.answer("Вы можете изменить следующие настройки:", reply_markup=settings_kb_ru)


# "Telefon raqamni o'zgartirish" ni bosganda
@router.message(text=["📞 Telefon raqamni o'zgartirish", "📞 Изменить номер телефона"])
async def change_phone_number(message: Message, state: FSMContext):
    lang = LanguageMiddleware.get_language(message.from_user.id)
    if lang == "uz":
        await message.answer("Iltimos, yangi telefon raqamingizni +998 ** *** ** ** shaklida kiriting:")
    elif lang == "ru":
        await message.answer("Пожалуйста, введите ваш новый номер телефона в формате +998 ** *** ** **.")
    await state.set_state(SettingsState.phone_change)


# Telefon raqamini tasdiqlash va bosh menyuga qaytish
@router.message(state=SettingsState.phone_change)
async def handle_phone_change(message: Message, state: FSMContext):
    contact_number = message.text.strip()
    lang = LanguageMiddleware.get_language(message.from_user.id)

    # Telefon raqamini tekshirish
    if contact_number.startswith("+998") and len(contact_number[4:]) == 9 and contact_number[4:].isdigit():
        # Foydalanuvchining telefon raqami o'zgartirildi
        await state.update_data(contact_number=contact_number)

        # Adminni xabardor qilish
        admin_message = f"📩 Foydalanuvchi {message.from_user.id} ning telefon raqami o'zgartirildi: {contact_number}"
        await message.bot.send_message(ADMIN_ID, admin_message)

        if lang == "uz":
            await message.answer("Telefon raqamingiz muvaffaqiyatli o'zgartirildi!", reply_markup=settings_kb_uz)
        elif lang == "ru":
            await message.answer("Ваш номер телефона успешно изменен!", reply_markup=settings_kb_ru)

        await state.finish()  # Bosh menu
    else:
        if lang == "uz":
            await message.answer("Telefon raqami noto'g'ri formatda! Iltimos, to'g'ri formatda kiriting.")
        elif lang == "ru":
            await message.answer("Номер телефона в неправильном формате! Пожалуйста, введите правильно.")
        await state.set_state(SettingsState.phone_change)


# "Tilni o'zgartirish" ni bosganda
@router.message(text=["🌍 Tilni o'zgartirish", "🌍 Изменить язык"])
async def change_language(message: Message, state: FSMContext):
    # Determine the user's current language
    lang = LanguageMiddleware.get_language(message.from_user.id)

    # Define the language selection keyboards
    lang_kb_uz = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🇺🇿 O'zbek"), KeyboardButton(text="🇷🇺 Русский")],
        ],
        resize_keyboard=True
    )
    lang_kb_ru = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🇺🇿 Узбек"), KeyboardButton(text="🇷🇺 Русский")],
        ],
        resize_keyboard=True
    )

    # Respond based on the user's current language
    if lang == "uz":
        await message.answer("Iltimos, tilni tanlang:", reply_markup=lang_kb_uz)
    elif lang == "ru":
        await message.answer("Пожалуйста, выберите язык:", reply_markup=lang_kb_ru)

    # Set the state to handle language selection
    await state.set_state(SettingsState.language_change)


# Tilni o'zgartirish
@router.message(state=SettingsState.language_change)
async def handle_language_change(message: Message, state: FSMContext):
    language = message.text.strip().lower()
    if language == "o'zbek" or language == "узбек":
        await state.update_data(language="uz")
    elif language == "русский":
        await state.update_data(language="ru")

    lang = LanguageMiddleware.get_language(message.from_user.id)
    if lang == "uz":
        await message.answer("Til muvaffaqiyatli o'zgartirildi!", reply_markup=settings_kb_uz)
    elif lang == "ru":
        await message.answer("Язык успешно изменен!", reply_markup=settings_kb_ru)
    await state.finish()  # Bosh menu


# "Ismni o'zgartirish" ni bosganda
@router.message(text=["✍️ Ismni o'zgartirish", "✍️ Изменить имя"])
async def change_name(message: Message, state: FSMContext):
    lang = LanguageMiddleware.get_language(message.from_user.id)
    if lang == "uz":
        await message.answer("Iltimos, yangi ismingizni kiriting:")
    elif lang == "ru":
        await message.answer("Пожалуйста, введите ваше новое имя:")
    await state.set_state(SettingsState.name_change)


# Ismni yangilash
@router.message(state=SettingsState.name_change)
async def handle_name_change(message: Message, state: FSMContext):
    new_name = message.text.strip()
    lang = LanguageMiddleware.get_language(message.from_user.id)

    # Foydalanuvchining ismini yangilash
    await state.update_data(name=new_name)

    # Adminni xabardor qilish
    admin_message = f"📩 Foydalanuvchi {message.from_user.id} ning ismi o'zgartirildi: {new_name}"
    await message.bot.send_message(ADMIN_ID, admin_message)

    if lang == "uz":
        await message.answer("Ismingiz muvaffaqiyatli o'zgartirildi!", reply_markup=settings_kb_uz)
    elif lang == "ru":
        await message.answer("Ваше имя успешно изменено!", reply_markup=settings_kb_ru)

    await state.finish()


# "Tug'ilgan kunni qo'shish" ni bosganda
@router.message(text=["🎂 Tug'ilgan kunni qo'shish", "🎂 Добавить дату рождения"])
async def change_birthday(message: Message, state: FSMContext):
    lang = LanguageMiddleware.get_language(message.from_user.id)
    if lang == "uz":
        await message.answer("Iltimos, tug'ilgan kuningizni DD-MM-YYYY formatida kiriting:")
    elif lang == "ru":
        await message.answer("Пожалуйста, введите вашу дату рождения в формате DD-MM-YYYY.")
    await state.set_state(SettingsState.birthday_change)


# Tug'ilgan kunni o'zgartirish
@router.message(state=SettingsState.birthday_change)
async def handle_birthday_change(message: Message, state: FSMContext, ADMIN_ID=None):
    birthday = message.text.strip()
    lang = LanguageMiddleware.get_language(message.from_user.id)

    # Tug'ilgan kunni tekshirish
    try:
        from datetime import datetime
        datetime.strptime(birthday, "%d-%m-%Y")  # To'g'ri formatda ekanligini tekshirish
        await state.update_data(birthday=birthday)

        # Adminni xabardor qilish
        admin_message = f"📩 Foydalanuvchi {message.from_user.id} ning tug'ilgan kuni o'zgartirildi: {birthday}"
        await message.bot.send_message(ADMIN_ID, admin_message)

        if lang == "uz":
            await message.answer("Tug'ilgan kuningiz muvaffaqiyatli qo'shildi!", reply_markup=settings_kb_uz)
        elif lang == "ru":
            await message.answer("Ваша дата рождения успешно добавлена!", reply_markup=settings_kb_ru)

        await state.finish()
    except ValueError:
        if lang == "uz":
            await message.answer("Siz noto'g'ri formatda kiritdingiz! Iltimos, DD-MM-YYYY formatida kiriting.")
        elif lang == "ru":
            await message.answer("Вы ввели неправильный формат! Пожалуйста, введите в формате DD-MM-YYYY.")
        await state.set_state(SettingsState.birthday_change)


# "Orqaga" tugmasi bosganda
@router.message(text=["🔙 Orqaga", "🔙 Назад"])
async def go_back_to_main_menu(message: Message, state: FSMContext):
    lang = LanguageMiddleware.get_language(message.from_user.id)
    if lang == "uz":
        await message.answer("Bosh menu:", reply_markup=settings_kb_uz)
    elif lang == "ru":
        await message.answer("Главное меню:", reply_markup=settings_kb_ru)
    await state.finish()
