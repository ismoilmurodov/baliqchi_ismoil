from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from back_end import get_categories
from handlers.order import OrderProcess
from keyboard.kb_menu import create_default_keyboard
from keyboard.kb_order import generate_payment_keyboard
from middlewares import LanguageMiddleware
from state.order_state import OrderState

router = Router()


# Обработчик изменений количества товара в корзине
@router.callback_query(lambda c: c.data.startswith("order"))
async def order_han(callback_query: CallbackQuery, state: FSMContext):
    # print(callback_query.data)
    await callback_query.message.delete()
    await callback_query.message.answer("Пожалуйста, выберите тип оплаты", reply_markup=generate_payment_keyboard())


# Обработчик очистки корзины
@router.callback_query(lambda c: c.data.startswith("clear_cart"))
async def clear_cart_handler(callback_query: CallbackQuery, state: FSMContext):
    print('clear_cart')
    # Очистим корзину в состоянии
    await state.update_data(order_products={})
    await callback_query.answer("Ваша корзина очищена." if LanguageMiddleware.get_language(
        callback_query.from_user.id) == 'ru' else "Сизнинг корзинангиз тозаланган.")
    await callback_query.message.answer("Korzinka tozalandi, qayta zakaz qilishingiz mumkin!",
                                        reply_markup=get_categories())


# Обработчик удаления товара из корзины
@router.callback_query(lambda c: c.data.startswith("delete_"))
async def delete_product_handler(callback_query: CallbackQuery, state: FSMContext):
    product_id = callback_query.data.split('_')[1]  # Получаем ID продукта из callback данных
    data = await state.get_data()
    lang = LanguageMiddleware.get_language(callback_query.from_user.id)

    # Если в корзине нет продуктов, ничего не делаем
    if 'order_products' not in data or product_id not in data['order_products']:
        await callback_query.answer("Продукт не найден в корзине.")
        return

    # Удаляем товар из корзины
    order_products = data['order_products']
    del order_products[product_id]
    await state.update_data(order_products=order_products)

    await callback_query.answer("Товар удален из корзины." if LanguageMiddleware.get_language(
        callback_query.from_user.id) == 'ru' else "Махсулот корзинадан ўчирилди.")

    data = ['📥 Korzinka'] if lang == 'uz' else ['📥 Корзина']

    categories = get_categories()
    data += [category['name'] for category in categories['categories']]

    data += ["⬅️ Qaytish"] if lang == 'uz' else ["⬅️ Назад"]
    keyboard = create_default_keyboard(data)

    confirmation_text = "Kategoriyalarni tanlang" if lang == 'uz' else "Выбирайте категории"
    await callback_query.message.answer(confirmation_text, reply_markup=keyboard)
    await state.set_state(OrderState.category)
