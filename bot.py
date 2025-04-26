from telebot import TeleBot
from buttons import *
from geopy import Photon
bot = TeleBot("7671651212:AAFLNOKURS6o7mQBNrvbt49Jgmqo82MaIqo")
# объект работающий с локацией
geolocator = Photon(user_agent="geo-locator", timeout=10)
@bot.message_handler(commands=["start"])
def start(message):
    user_id = message.from_user.id
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
        bot.send_message(user_id, f"Вы успешно прошли регистрацию, {name}!\n"
                                  f"Ваш номер: {phone_number}")
        bot.send_message(user_id, "Отправьте свою локацию", reply_markup=location_bt())
        bot.register_next_step_handler(message, get_location)
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



bot.infinity_polling()