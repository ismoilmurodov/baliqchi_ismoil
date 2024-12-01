import re
from datetime import datetime


def validate_phone_number(contact_number):
    if contact_number.startswith("994") and not contact_number.startswith("+"):
        contact_number = "+998" + contact_number[3:]

    if re.match(r"^\+998\d{9}$", contact_number):
        return contact_number
    else:
        return None


def convert_to_yyyy_mm_dd(date_str):
    try:
        date_object = datetime.strptime(date_str, "%d-%m-%Y")
        return date_object.strftime("%Y-%m-%d")
    except ValueError:
        raise ValueError(f"Invalid date format: {date_str}. Expected format is DD-MM-YYYY.")



# Форматирование товаров в корзине
def format_order_products(order_products):
    formatted_order = []
    for product, quantity in order_products.items():
        formatted_order.append(f"{quantity} ✖️ {product}")
    return "\n".join(formatted_order)
