from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types import Message

from back_end import get_categories, fetch_products_by_category, fetch_product_details
from handlers.menu import create_default_keyboard
from keyboards import main_menu_kb, main_menu_kb_ru
from middlewares import LanguageMiddleware
from state.order_state import OrderState

router = Router()


@router.message(OrderState.category)
async def product_handler(message: Message, state: FSMContext):
    lang = LanguageMiddleware.get_language(message.from_user.id)

    if message.text in ["⬅️ Qaytish", "⬅️ Назад"]:
        message_context = "Asosiy menu" if lang == 'uz' else "Выбирайте категории"
        await message.answer(message_context, reply_markup=main_menu_kb if lang == 'uz' else main_menu_kb_ru)
        await state.clear()

    else:
        category = message.text
        await state.update_data(category=category)

        products = await fetch_products_by_category(category)
        data = [product['name'] for product in products]
        data += ["⬅️ Qaytish"] if lang == 'uz' else ["⬅️ Назад"]
        keyboard = create_default_keyboard(data)

        m_contest = "Maxsulotlar" if lang == 'uz' else "Продукты"

        await message.answer(m_contest, reply_markup=keyboard)

        await state.set_state(OrderState.product)


@router.message(OrderState.product)
async def product_order_handler(message: Message, state: FSMContext):
    lang = LanguageMiddleware.get_language(message.from_user.id)
    if message.text in ["⬅️ Qaytish", "⬅️ Назад"]:
        data = ['📥 Korzinka'] if lang == 'uz' else ['📥 Корзина']

        categories = get_categories()
        data += [category['name'] for category in categories['categories']]

        data += ["⬅️ Qaytish"] if lang == 'uz' else ["⬅️ Назад"]
        keyboard = create_default_keyboard(data)

        confirmation_text = "Kategoriyalarni tanlang" if lang == 'uz' else "Выбирайте категории"
        print(data)
        await message.answer(confirmation_text, reply_markup=keyboard)
        await state.set_state(OrderState.category)
    else:
        product_name = message.text
        await state.update_data(product=product_name)

        # Retrieve the saved category from state
        data = await state.get_data()
        category = data.get('category')

        product_data = await fetch_product_details(category, product_name)

        if product_data:
            # Extract product details
            product_name = product_data.get('name', 'Unknown Product')
            description = product_data.get('description', 'No description available')
            price = product_data.get('price', '0')
            image_url = f"http://talaba.turin.uz{product_data.get('image', '')}"

            product_caption = f"✨ <b>Название:</b> {product_name}\n" \
                              f"📜 <b>Описание:</b> {description}\n" \
                              f"💲 <b>Итог:</b> {price} UZS\n"

            # Set initial quantity to 1
            quantity = 1
            kb_name = "⬅️ Qaytish" if lang == 'uz' else "⬅️ Назад"
            kb_back = ReplyKeyboardMarkup(
                keyboard=[[KeyboardButton(text=kb_name)]],
                resize_keyboard=True
            )
            await message.answer("Выберите количество продукта", reply_markup=kb_back)
            # Create the inline keyboard with product options
            inline_keyboard = create_inline_keyboard(product_name, quantity)

            # Send the product details with image and inline buttons
            await message.answer_photo(image_url, caption=product_caption, reply_markup=inline_keyboard,
                                       parse_mode='HTML')
            await state.set_state(OrderState.back)
        else:
            await message.answer("Sorry, we couldn't retrieve the product details. Please try again later.")


# Helper function to create inline keyboard
def create_inline_keyboard(product_name, quantity):
    button_decrease = InlineKeyboardButton(text="➖", callback_data=f"quantity_decrease_{product_name}")
    button_quantity = InlineKeyboardButton(text=str(quantity), callback_data="quantity_current")
    button_increase = InlineKeyboardButton(text="➕", callback_data=f"quantity_increase_{product_name}")
    button_add_to_cart = InlineKeyboardButton(text="🛒 Добавить в корзинку", callback_data=f"add_to_cart_{product_name}")

    return InlineKeyboardMarkup(row_width=3, inline_keyboard=[
        [button_decrease, button_quantity, button_increase],
        [button_add_to_cart]
    ])


@router.message(OrderState.back)
async def back_handler(message: Message, state: FSMContext):
    lang = LanguageMiddleware.get_language(message.from_user.id)

    data = await state.get_data()
    category = data['category']
    products = await fetch_products_by_category(category)
    data = [product['name'] for product in products]
    data += ["⬅️ Qaytish"] if lang == 'uz' else ["⬅️ Назад"]
    keyboard = create_default_keyboard(data)

    m_contest = "Maxsulotlar" if lang == 'uz' else "Продукты"

    await message.answer(m_contest, reply_markup=keyboard)

    await state.set_state(OrderState.product)


# Callback handler for quantity changes (decrease, increase)
@router.callback_query(OrderState.back, lambda c: c.data.startswith("quantity_"))
async def handle_quantity_change(callback_query: CallbackQuery, state: FSMContext):
    action = "_".join(callback_query.data.split("_")[:2])
    product_name = callback_query.data.split("_")[2]  # Product name

    # Retrieve current quantity from FSM state
    current_data = await state.get_data()
    quantity = current_data.get(product_name, 1)  # Default to 1 if no stored quantity

    if action == "quantity_decrease":
        quantity -= 1
    elif action == "quantity_increase":
        quantity += 1

    # Ensure the quantity doesn't go below 1
    if quantity < 1:
        quantity = 1

    # Store updated quantity in FSM state
    await state.update_data({product_name: quantity})

    # Generate the updated inline keyboard
    inline_keyboard = create_inline_keyboard(product_name, quantity)

    # Check if the current message's reply_markup is different from the new one
    if callback_query.message.reply_markup != inline_keyboard:
        # Send the updated inline keyboard to the user
        await callback_query.answer(f"Количество для {product_name} теперь равно {quantity}.")
        await callback_query.message.edit_reply_markup(reply_markup=inline_keyboard)
    else:
        # If markup is the same, just answer without editing the message
        await callback_query.answer(f"Количество для {product_name} уже равно {quantity}.")


@router.callback_query(lambda c: c.data.startswith("add_to_cart"))
async def add_to_cart(callback_query: CallbackQuery, state: FSMContext):
    product_name = callback_query.data.split("_")[2]  # Extract product name

    # Retrieve the current quantity from FSM state
    current_data = await state.get_data()
    quantity = current_data.get(product_name, 1)  # Default to 1 if no quantity is set

    # Retrieve or initialize cart
    cart = current_data.get("cart", {})  # Get cart from state or default to empty dictionary

    # Update the cart with the selected product and its quantity
    try:
        cart[product_name] = cart.get(product_name, 0) + quantity
    except:
        cart[product_name] = 1
    # Save the updated cart to FSM state
    await state.update_data(cart=cart)

    # Acknowledge the user that the product was added to the cart
    await callback_query.answer(f"{product_name} ({quantity} pcs) added to your cart!")

    # Delete the message showing the product details
    await callback_query.message.delete()

    # Optionally send the order summary (if needed)
    order_message = f"Ваш заказ обновлен:\n\nХотите продолжить оформление заказа?"

    await callback_query.message.answer(order_message)

    lang = LanguageMiddleware.get_language(callback_query.from_user.id)

    if lang == "uz":
        confirmation_text = "Kategoriyalarni tanlang"
        data = ['📥 Korzinka']
    elif lang == "ru":
        confirmation_text = "Выбирайте категории"
        data = ['📥 Корзина']

    categories = get_categories()
    data += [category['name'] for category in categories['categories']]

    keyboard = create_default_keyboard(data)
    print("confirmation_text: ", confirmation_text)
    await callback_query.message.answer(f"{confirmation_text}", reply_markup=keyboard)

    await state.set_state(OrderState.category)
