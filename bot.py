from telebot import TeleBot
from buttons import *
import database as db
from geopy import Photon
bot = TeleBot(token="TOKEN")
# db.add_product("Чикенбургер", 30000.0, "вкусная курочка в булочке", 10, "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTYO_gzNUj6uWpQZRLLTQSb_tGBrLZaUV-Uew&s")
# db.add_product("Даблбургер", 50000.0, "две вкусные котлеты в булочке", 10, "https://d2j6dbq0eux0bg.cloudfront.net/images/14450072/1156014693.jpg")
# db.add_product("Хот-дог", 20000.0, "сосиска в булочке", 0, "https://d2j6dbq0eux0bg.cloudfront.net/images/14450072/1156014693.jpg")
# временная корзина {user_id:{pr_id, pr_name, pr_count, pr_price}}
users = {}
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
@bot.callback_query_handler(lambda call: call.data in ["back", "cart",
                                                       "plus", "minus", "to_cart",
                                                       "back_product", "cart",
                                                       "order", "clear_cart"])
def calls(call):
    user_id = call.message.chat.id
    if call.data == "back":
        bot.delete_message(user_id, call.message.message_id)
        bot.send_message(user_id, "Главное меню:", reply_markup=main_menu_bt())
    elif call.data == "plus":
        current_amount = users.get(user_id).get("pr_count")
        users[user_id]["pr_count"] += 1
        bot.edit_message_reply_markup(user_id, call.message.message_id,
                                      reply_markup=plus_minus_in("plus", current_amount))
    elif call.data == "minus":
        current_amount = users.get(user_id).get("pr_count")
        if current_amount > 1:
            users[user_id]["pr_count"] -= 1
            bot.edit_message_reply_markup(user_id, call.message.message_id,
                                          reply_markup=plus_minus_in("minus", current_amount))
    elif call.data == "to_cart":
        db.add_to_cart(user_id, users.get(user_id).get("pr_id"),
                       users.get(user_id).get("pr_name"),
                       users.get(user_id).get("pr_price"),
                       users.get(user_id).get("pr_count"))
        users.pop(user_id)
        bot.delete_message(user_id, call.message.message_id)
        all_products = db.get_products_id_name()
        bot.send_message(user_id, "Продукт добавлен в корзину. Хотите выбрать что-нибудь еще? ",
                         reply_markup=all_products_in(all_products))
    elif call.data == "back_product":
        bot.delete_message(user_id, call.message.message_id)
        all_products = db.get_products_id_name()
        bot.send_message(user_id, "Выберите продукт: ",
                         reply_markup=all_products_in(all_products))
    elif call.data == "cart":
        bot.delete_message(user_id, call.message.message_id)
        cart = db.get_user_cart(user_id)
        full_text = "Ваша корзина:\n"
        count = 0
        total_price = 0
        for product in cart:
            count += 1
            full_text += f"{count}. {product[0]} x {product[1]} = {product[2]} сум\n"
            total_price += product[2]
        full_text += f"\nИтоговая сумма: {total_price} сум"
        bot.send_message(user_id, full_text, reply_markup=cart_in())
    elif call.data == "clear_cart":
        db.delete_user_cart(user_id)
        bot.delete_message(user_id, call.message.message_id)
        all_products = db.get_products_id_name()
        bot.send_message(user_id, "Корзина очищена. Хотите что-нибудь заказать?: ",
                         reply_markup=all_products_in(all_products))
    elif call.data == "order":
        bot.delete_message(user_id, call.message.message_id)
        cart = db.get_user_cart(user_id)
        full_text = f"Новый заказ от юзера {user_id}:\n"
        count = 0
        total_price = 0
        for product in cart:
            count += 1
            full_text += f"{count}. {product[0]} x {product[1]} = {product[2]} сум\n"
            total_price += product[2]
        full_text += f"\nИтоговая сумма: {total_price} сум"
        bot.send_message(-4789605501, full_text, reply_markup=user_info_in(user_id))
        db.delete_user_cart(user_id)
        bot.send_message(user_id, "Ваш заказ принят. Ожидайте подтверждения",
                         reply_markup=main_menu_bt())

@bot.callback_query_handler(lambda call: "info_" in call.data)
def get_user_info(call):
    user_id = call.message.chat.id
    info_id = int(call.data.replace("info_", ""))
    info = db.get_user_info(info_id)
    bot.answer_callback_query(call.id, text=f"Имя пользователя: {info[0]}\n"
                                            f"Номер пользователя: {info[1]}")

# функция для удаления одного продукта из корзины
@bot.callback_query_handler(lambda call: "delete_" in call.data)
def delete_prod_from_cart(call):
    bot.edit_message_text()
    # удаление + сенд_месседж
    ...

@bot.callback_query_handler(lambda call: "prod_" in call.data)
def get_prod_info(call):
    user_id = call.message.chat.id
    bot.delete_message(user_id, call.message.message_id)
    pr_id = int(call.data.replace("prod_", ""))
    product_info = db.get_exact_product(pr_id)
    #pr_name, pr_price, pr_desc, pr_photo
    # передача информации во временную корзину
    users[user_id] = {"pr_id": pr_id, "pr_name": product_info[0], "pr_count": 1,
                      "pr_price": product_info[1]}
    bot.send_photo(user_id, photo=product_info[3], caption=f"{product_info[0]}\n"
                                                           f"Цена: {product_info[1]}\n"
                                                           f"Описание: {product_info[2]}\n",
                   reply_markup=plus_minus_in())
@bot.message_handler(content_types=["text"])
# обработчик обычных кнопок
def text_func(message):
    user_id = message.from_user.id
    text = message.text
    if text == "🍴Меню":
        # запрашиваем все продукты для кнопок
        all_products = db.get_products_id_name()
        bot.send_message(user_id, "Выберите продукт: ",
                        reply_markup=all_products_in(all_products))
    elif text == "🛒Корзина":
        bot.send_message(user_id, "Ваша корзина: ")
    elif text == "✍Оставить отзыв":
        bot.send_message(user_id, "Напишите ваш отзыв: ")
        bot.register_next_step_handler(message, send_feedback)
    elif text == "⚙️Настройки":
        bot.send_message(user_id, "Что хотите изменить?")
def send_feedback(message):
    user_id = message.from_user.id
    admin_id = -4789605501
    bot.send_message(admin_id, f"Новый отзыв от юзера с ID {user_id}:\n\n"
                               f"{message.text}")
bot.infinity_polling()