from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup
from geopy.geocoders import Nominatim

from back_end import get_categories
from keyboard.kb_menu import location_kb_uz, location_kb_ru, create_default_keyboard
from keyboards import main_menu_kb, main_menu_kb_ru
from middlewares import LanguageMiddleware
from state.order_state import OrderState

router = Router()

geolocator = Nominatim(user_agent="my_bot")


@router.message(lambda message: message.text in ["📋 Menu", "📋 Меню"])
async def show_location_menu(message: Message):
    lang = LanguageMiddleware.get_language(message.from_user.id)
    message_context = "Kerakli bo'limni tanlang: " if lang == 'uz' else "Выберите нужный раздел:"
    kb = location_kb_uz if lang == 'uz' else location_kb_ru
    await message.answer(message_context, reply_markup=kb)


@router.message(lambda message: message.text in ["📍 Joylashuvlar ro'yxati", "📍 Список местоположений"])
async def send_location_list(message: Message):
    lang = LanguageMiddleware.get_language(message.from_user.id)
    message_context = "Joylashuvlar ro'yxati: kerakli manzilni tanlang." if lang == 'uz' else "Список местоположений: выберите нужное место."
    kb_name = "⬅️ Qaytish" if lang == 'uz' else "⬅️ Назад"
    kb = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=kb_name)]],
        resize_keyboard=True
    )
    await message.answer(message_context, reply_markup=kb)


@router.message(lambda message: message.text in ["⬅️ Qaytish", "⬅️ Назад"])
async def send_location_request(message: Message):
    lang = LanguageMiddleware.get_language(message.from_user.id)
    message_context = "Asosiy menu!" if lang == 'uz' else "Главное меню!"
    kb = main_menu_kb if lang == 'uz' else main_menu_kb_ru
    await message.answer(message_context, reply_markup=kb)


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
    else:
        await message.answer(f"Ваш адрес: {address}\n\nВаше местоположение подтверждено! ✅")

    # Button
    data = ['📥 Korzinka'] if lang == 'uz' else ['📥 Корзина']
    categories = get_categories()
    data += [category['name'] for category in categories['categories']]
    data += ['⬅️ Qaytish'] if lang == 'uz' else ['⬅️ Назад']

    keyboard = create_default_keyboard(data)
    confirmation_text = "Kategoriyalarni tanlang" if lang == 'uz' else "Выбирайте категории"
    await message.answer(confirmation_text, reply_markup=keyboard)

    await state.set_state(OrderState.category)
