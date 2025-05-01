from telebot import types

def phone_number_bt():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton("Отправить номер", request_contact=True)
    kb.add(button1)
    return kb
def location_bt():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton("Отправить локацию", request_location=True)
    kb.add(button1)
    return kb
def main_menu_bt():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    products = types.KeyboardButton("🍴Меню")
    cart = types.KeyboardButton("🛒Корзина")
    feedback = types.KeyboardButton("✍Оставить отзыв")
    settings = types.KeyboardButton("⚙️Настройки")
    # по две кнопки в ряд
    kb.row(products, cart)
    kb.row(feedback, settings)
    return kb
def all_products_in(all_products):
    kb = types.InlineKeyboardMarkup(row_width=2)
    # статичные(постоянные кнопки)
    cart = types.InlineKeyboardButton(text="Корзина", callback_data="cart")
    back = types.InlineKeyboardButton(text="Назад", callback_data="back")
    # динамичные кнопки ...
    all_products_button = [types.InlineKeyboardButton(text=product[1], callback_data=f"prod_{product[0]}") for product in all_products]
    kb.add(*all_products_button)
    kb.row(cart)
    kb.row(back)
    return kb
def plus_minus_in(plus_or_minus="", current_amount=1):
    kb = types.InlineKeyboardMarkup(row_width=3)
    # статичные кнопки
    to_cart = types.InlineKeyboardButton(text="Добавить в корзину", callback_data="to_cart")
    back = types.InlineKeyboardButton(text="Назад", callback_data="back_product")
    plus = types.InlineKeyboardButton(text="➕", callback_data="plus")
    minus = types.InlineKeyboardButton(text="➖", callback_data="minus")
    count = types.InlineKeyboardButton(text=str(current_amount), callback_data="none")
    # изменение кнопок
    if plus_or_minus == "plus":
        count = types.InlineKeyboardButton(text=f"{current_amount + 1}", callback_data="none")
    elif plus_or_minus == "minus" and current_amount > 1:
        count = types.InlineKeyboardButton(text=f"{current_amount - 1}", callback_data="none")
    kb.row(minus, count, plus)
    kb.row(to_cart)
    kb.row(back)
    return kb