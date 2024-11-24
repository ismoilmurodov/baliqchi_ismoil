from aiogram import Router
from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from geopy.geocoders import Nominatim

from back_end import get_categories
from keyboard.kb_menu import location_kb_uz, location_kb_ru
from middlewares import LanguageMiddleware
from state.order_state import OrderState

router = Router()

geolocator = Nominatim(user_agent="my_bot")


# Пример добавления кнопки для отправки геолокации
async def create_location_keyboard(lang: str):
    if lang == "uz":
        return ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="📍 Joylashuvni yuborish", request_location=True)]
            ],
            resize_keyboard=True
        )
    elif lang == "ru":
        return ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="📍 Отправить местоположение", request_location=True)]
            ],
            resize_keyboard=True
        )


@router.message(lambda message: message.text in ["📋 Menu", "📋 Меню"])
async def show_location_menu(message: Message, state: FSMContext):
    lang = LanguageMiddleware.get_language(message.from_user.id)

    if lang == "uz":
        await message.answer("Kerakli bo'limni tanlang:", reply_markup=location_kb_uz)
    elif lang == "ru":
        await message.answer("Выберите нужный раздел:", reply_markup=location_kb_ru)


@router.message(lambda message: message.text in ["📍 Joylashuvlar ro'yxati", "📍 Список местоположений"])
async def send_location_list(message: Message, state: FSMContext):
    lang = LanguageMiddleware.get_language(message.from_user.id)
    if lang == "uz":
        await message.answer("Joylashuvlar ro'yxati: kerakli manzilni tanlang.")
    elif lang == "ru":
        await message.answer("Список местоположений: выберите нужное место.")


@router.message(lambda message: message.text in ["📍 Joylashuvni yuborish", "📍 Отправить местоположение"])
async def send_location_request(message: Message, state: FSMContext):
    lang = LanguageMiddleware.get_language(message.from_user.id)
    location_keyboard = await create_location_keyboard(lang)

    if lang == "uz":
        await message.answer("Iltimos, joylashuvni yuboring!", reply_markup=location_keyboard)

    elif lang == "ru":
        await message.answer("Пожалуйста, пришлите местоположение!", reply_markup=location_keyboard)


def create_default_keyboard(kb_buttons_list):
    keyboard = ReplyKeyboardBuilder()
    for kb_button in kb_buttons_list:
        keyboard.add(types.KeyboardButton(text=kb_button))
        keyboard.row()
    return keyboard.adjust(1, repeat=True).as_markup(resize_keyboard=True)


@router.message(lambda message: message.location is not None)
async def confirm_location(message: Message, state: FSMContext):
    lang = LanguageMiddleware.get_language(message.from_user.id)

    latitude = message.location.latitude
    longitude = message.location.longitude

    location = geolocator.reverse((latitude, longitude), language='uz')

    if location:
        address = location.address
    else:
        await message.answer("Извините, я не смог определить ваше местоположение.")
        return

    if lang == "uz":
        await message.answer(f"Sizning manzilingiz: {address}\n\nJoylashuvingiz tasdiqlandi! ✅")
        confirmation_text = "Kategoriyalarni tanlang"
        data = ['📥 Korzinka']
    elif lang == "ru":
        await message.answer(f"Ваш адрес: {address}\n\nВаше местоположение подтверждено! ✅")
        confirmation_text = "Выбирайте категории"
        data = ['📥 Корзина']

    categories = get_categories()
    data += [category['name'] for category in categories['categories']]

    keyboard = create_default_keyboard(data)

    await message.answer(confirmation_text, reply_markup=keyboard)

    await state.set_state(OrderState.category)
