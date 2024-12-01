from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import Message

from back_end import get_categories, fetch_products_by_category, fetch_product_details
from handlers.menu import create_default_keyboard
from keyboard.kb_order import order_message, generate_cart_keyboard, create_inline_keyboard
from keyboards import main_menu_kb, main_menu_kb_ru
from middlewares import LanguageMiddleware
from state.order_state import OrderState, OrderProcess
from utils import format_order_products

router = Router()


# Обработчик выбора категории товара
@router.message(OrderState.category)
async def product_handler(message: Message, state: FSMContext):
    lang = LanguageMiddleware.get_language(message.from_user.id)

    if message.text in ["⬅️ Qaytish", "⬅️ Назад"]:
        message_context = "Asosiy menu" if lang == 'uz' else "Выбирайте категории"
        await message.answer(message_context, reply_markup=main_menu_kb if lang == 'uz' else main_menu_kb_ru)
        await state.clear()

    # Обработка корзины
    elif message.text in ['📥 Korzinka', '📥 Корзина']:
        data = await state.get_data()
        print(data)

        # Если корзина пуста
        if 'order_products' not in data or not data['order_products']:
            await message.answer("Ваша корзина пуста." if lang == 'ru' else "Сизнинг корзинангиз бўш.")
            return

        try:
            order_products_str = format_order_products(data['order_products'])
        except Exception as e:
            await message.answer("Ошибка при обработке корзины. Попробуйте снова.")
            return

        data['total_price'] = 10000  # Стоимость товаров
        data['delivery_price'] = 20000  # Стоимость доставки

        # Пример расчета итоговой стоимости
        message_text = order_message(data['total_price'], data['delivery_price'], order_products_str)
        await message.answer(message_text, reply_markup=generate_cart_keyboard(data['order_products']))
        # await state.set_state(OrderProcess.order_type)

    else:
        category = message.text
        await state.update_data(category=category)

        # Получаем продукты по выбранной категории
        products = await fetch_products_by_category(category)
        data = [product['name'] for product in products]
        data += ["⬅️ Qaytish"] if lang == 'uz' else ["⬅️ Назад"]
        keyboard = create_default_keyboard(data)

        m_contest = "Maxsulotlar" if lang == 'uz' else "Продукты"
        await message.answer(m_contest, reply_markup=keyboard)

        # Инициализируем корзину, если она еще не создана
        data = await state.get_data()
        if 'order_products' not in data:
            await state.update_data(order_products={})

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
        await message.answer(confirmation_text, reply_markup=keyboard)

        await state.set_state(OrderState.category)
    else:
        product_name = message.text
        await state.update_data(product=product_name)

        data = await state.get_data()
        category = data.get('category')

        product_data = await fetch_product_details(category, product_name)

        if product_data:
            # Extract product details
            product_name = product_data.get('name', 'Unknown Product')
            description = product_data.get(
                'description', 'No description available')
            price = product_data.get('price', '0')
            image_url = f"http://talaba.turin.uz{
            product_data.get('image', '')}"

            product_caption = f"✨ <b>Название:</b> {product_name}\n" \
                              f"📜 <b>Описание:</b> {description}\n" \
                              f"💲 <b>Сумма:</b> {price} UZS\n"

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

    # Retrieve current quantity from FSM state
    current_data = await state.get_data()
    # Default to 1 if no stored quantity
    try:
        quantity = current_data['quantity']
    except:
        quantity = 1

    if action == "quantity_decrease":
        quantity -= 1
    elif action == "quantity_increase":
        quantity += 1

    # Ensure the quantity doesn't go below 1
    if quantity < 1:
        quantity = 1

    await state.update_data(quantity=quantity)

    # Generate the updated inline keyboard
    inline_keyboard = create_inline_keyboard(current_data['product'], quantity)

    # Check if the current message's reply_markup is different from the new one

    if callback_query.message.reply_markup != inline_keyboard:
        # Send the updated inline keyboard to the user
        await callback_query.answer(f"Количество для {current_data['product']} теперь равно {quantity}.")
        await callback_query.message.edit_reply_markup(reply_markup=inline_keyboard)
    else:
        # If markup is the same, just answer without editing the message
        await callback_query.answer(f"Количество для {current_data['product']} уже равно {quantity}.")


@router.callback_query(lambda c: c.data.startswith("add_to_cart"))
async def add_to_cart(callback_query: CallbackQuery, state: FSMContext):
    product_name = callback_query.data.split("_")[2]  # Extract product name

    current_data = await state.get_data()
    print("curret_data: ", current_data)

    try:
        current_data['order_products'][current_data['product']
        ] = current_data['quantity']
    except:
        current_data['quantity'] = 1
        current_data['order_products'][current_data['product']] = 1
    print(current_data)

    await state.update_data(order_products=current_data['order_products'])

    data = await state.get_data()
    print(data)

    # Acknowledge the user that the product was added to the cart
    await callback_query.answer(f"{product_name} ({current_data['quantity']} pcs) added to your cart!")

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
    data += ["⬅️ Qaytish"] if lang == 'uz' else ["⬅️ Назад"]

    keyboard = create_default_keyboard(data)
    print("confirmation_text: ", confirmation_text)
    data = await state.get_data()
    print(data)
    await callback_query.message.answer(f"{confirmation_text}", reply_markup=keyboard)

    await state.set_state(OrderState.category)
