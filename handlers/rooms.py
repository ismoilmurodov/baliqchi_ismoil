from aiogram import Router
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message

from handlers.menu import create_default_keyboard
from keyboards import main_menu_kb, main_menu_kb_ru
from middlewares import LanguageMiddleware

router = Router()


class RoomStateGroup(StatesGroup):
    cat = State()
    room = State()


@router.message(lambda message: message.text in ["🏨 Xonalar haqida ma'lumot", "🏨 Информация о номерах"])
async def room_info(message: Message, state: FSMContext):
    print(message.text)
    lang = LanguageMiddleware.get_language(message.from_user.id)

    url = "http://talaba.turin.uz/fish/api/v1/roomcategories/"
    response = requests.get(url)
    data = response.json()
    names = [item['name'] for item in data]
    print(names)
    print(lang)

    if lang == "uz":
        names.append("⬅️ Qaytish")
        keyboard = create_default_keyboard(names)
        await message.answer("Xonalar haqida ma'lumot", reply_markup=keyboard)

    elif lang == "ru":
        names.append("⬅️ Назад")
        keyboard = create_default_keyboard(names)
        await message.answer("Информация о номерах", reply_markup=keyboard)

    await state.set_state(RoomStateGroup.cat)


import requests


@router.message(RoomStateGroup.cat)
async def cat_handler(message: Message, state: FSMContext):
    await state.update_data(cat=message.text)
    # Get the user's preferred language
    lang = LanguageMiddleware.get_language(message.from_user.id)

    if message.text in ["⬅️ Qaytish", "⬅️ Назад"]:
        if lang == "uz":
            await message.answer("⬅️ Qaytish", reply_markup=main_menu_kb)
        else:
            await message.answer("️ Назад", reply_markup=main_menu_kb_ru)
        await state.clear()
        return
        # Prepare text based on the user's language
    if lang == "uz":
        no_rooms_found_text = "Kechirasiz, xona topilmadi."
        room_caption_template = """
<b>{room_name}</b> (Kategoriya: {room_category})
<i>{room_description}</i>
"""
    elif lang == "ru":
        no_rooms_found_text = "Извините, комнаты не найдены."
        room_caption_template = """
<b>{room_name}</b> (Категория: {room_category})
<i>{room_description}</i>
"""
    else:
        # Default text for unsupported languages (or English as fallback)
        no_rooms_found_text = "Sorry, no rooms found."
        room_caption_template = """
<b>{room_name}</b> (Category: {room_category})
<i>{room_description}</i>
"""

    # Retrieve category data from FSM context
    url = f"http://talaba.turin.uz/fish/api/v1/roomcategories/{message.text}/rooms/"

    # Fetch the room data from the API
    response = requests.get(url)
    room_data = response.json()  # Assuming this is the list of rooms you shared earlier

    # If there are rooms, send each room's image and information as a separate message
    if room_data:
        for room in room_data:
            room_id = room.get("id")
            room_name = room.get("name")
            room_description = room.get("description").replace("\r\n", "\n")  # Clean up newlines
            room_image = room.get("image")
            room_category = room.get("category")

            # Format the caption using the template for the current language
            caption = room_caption_template.format(
                room_name=room_name,
                room_category=room_category,
                room_description=room_description
            )

            # Send the image with the caption
            await message.answer_photo(
                photo=room_image,  # URL or file ID of the image
                caption=caption,  # Caption with formatted text
                parse_mode=ParseMode.HTML,  # Use HTML for formatting
                reply_markup=main_menu_kb if lang == 'uz' else main_menu_kb_ru
            )
    else:
        # If no rooms are found, send the appropriate message based on the language
        await message.answer(no_rooms_found_text)
        await state.clear()