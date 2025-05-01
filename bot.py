from telebot import TeleBot
from buttons import *
import database as db
from geopy import Photon
bot = TeleBot("7671651212:AAFLNOKURS6o7mQBNrvbt49Jgmqo82MaIqo")
# объект работающий с локацией
geolocator = Photon(user_agent="geo-locator", timeout=10)
@bot.message_handler(commands=["start"])
def start(message):
    user_id = message.from_user.id
    checker = db.check_user(user_id)
    if checker == True:
        bot.send_message(user_id, "Главное меню:", reply_markup=main_menu_bt())
    elif checker == False:
        bot.send_message(user_id, "Добро пожаловать в бот доставки!\n"
                                  "Пожалуйста, введите свое имя")
        bot.register_next_step_handler(message, get_name)
def get_name(message):
    user_id = message.from_user.id
    name = message.text
    bot.send_message(user_id, f"Отлично, {name}. Пожалуйста, отправьте свой номер",
                     reply_markup=phone_number_bt())
    # отправляем его в функцию получения номера вместе с информацией об имени
    bot.register_next_step_handler(message, get_phone, name)
# принимаю это имя в параметр name
def get_phone(message, name):
    user_id = message.from_user.id
    if message.contact:
        phone_number = message.contact.phone_number
        db.add_user(user_id, name, phone_number)
        bot.send_message(user_id, f"Вы успешно прошли регистрацию, {name}!\n"
                                  f"Ваш номер: {phone_number}")
        # bot.send_message(user_id, "Отправьте свою локацию", reply_markup=location_bt())
        # bot.register_next_step_handler(message, get_location)
    else:
        bot.send_message(user_id, "Отправьте свой номер через кнопку в меню.",
                         reply_markup=phone_number_bt())
        # отправляем пользователя в эту же функцию, пока он не отправить номер через кнопку
        bot.register_next_step_handler(message, get_phone, name)
def get_location(message):
    user_id = message.from_user.id
    if message.location:
        # получаем долготу и широту
        longitude = message.location.longitude
        latitude = message.location.latitude
        # преобразуем данные в адрес
        address = geolocator.reverse((latitude, longitude)).address
        bot.send_message(user_id, f"Ваш адрес: {address}")
    else:
        bot.send_message(user_id, "Отправьте локацию через кнопку в меню",
                         reply_markup=location_bt())
        bot.register_next_step_handler(message, get_location)

@bot.message_handler(content_types=["text"])
# обработчик обычных кнопок
def text_func(message):
    user_id = message.from_user.id
    text = message.text
    if text == "🍴Меню":
        bot.send_message(user_id, "Выберите продукт: ")
    elif text == "🛒Корзина":
        bot.send_message(user_id, "Ваша корзина: ")
    elif text == "✍Оставить отзыв":
        bot.send_message(user_id, "Напишите ваш отзыв: ")
    elif text == "⚙️Настройки":
        bot.send_message(user_id, "Что хотите изменить?")

bot.infinity_polling()