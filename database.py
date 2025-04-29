import sqlite3
from datetime import datetime
connection = sqlite3.connect("kfc.db")
sql = connection.cursor()
# создаем таблицу юзеров
sql.execute("CREATE TABLE IF NOT EXISTS users (user_id INTEGER, name TEXT,"
            "phone_number TEXT, reg_date DATETIME);")
# создаем таблицу продуктов
sql.execute("CREATE TABLE IF NOT EXISTS products (pr_id INTEGER PRIMARY KEY AUTOINCREMENT,"
            "pr_name TEXT, pr_price REAL, pr_desc TEXT, pr_photo TEXT, pr_quantity INTEGER,"
            "reg_date DATETIME);")
# создаем таблицу корзин пользователей
sql.execute("CREATE TABLE IF NOT EXISTS cart (user_id INTEGER, pr_id INTEGER, pr_name TEXT,"
            "pr_count INTEGER, total_price REAL);")
connection.commit()
# функции для юзеров
# добавление юзера
def add_user(user_id, name, phone_number):
    connection = sqlite3.connect("kfc.db")
    sql = connection.cursor()
    sql.execute(f"INSERT INTO users (user_id, name, phone_number, reg_date) "
                f"VALUES (?, ?, ?, ?);", (user_id, name, phone_number, datetime.now()))
    connection.commit()
# проверка зарегистрирован ли юзер
def check_user(user_id):
    connection = sqlite3.connect("kfc.db")
    sql = connection.cursor()
    check = sql.execute("SELECT * FROM users WHERE user_id=?;", (user_id, )).fetchone()
    # если юзер найден
    if check:
        return True
    # если юзер не найден
    elif not check:
        return False
# получение всех юзеров
def get_all_users():
    connection = sqlite3.connect("kfc.db")
    sql = connection.cursor()
    all_users = sql.execute("SELECT * FROM users;").fetchall()
    return all_users

# функции для работы с продуктами
# добавление продукта
def add_product(pr_name, pr_price, pr_desc, pr_quantity, pr_photo):
    connection = sqlite3.connect("kfc.db")
    sql = connection.cursor()
    sql.execute("INSERT INTO products (pr_name, pr_price, pr_desc, pr_quantity,"
                "pr_photo, reg_date) VALUES (?, ?, ?, ?, ?, ?);",
                (pr_name, pr_price, pr_desc, pr_quantity, pr_photo, datetime.now()))
    connection.commit()