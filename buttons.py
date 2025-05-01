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
