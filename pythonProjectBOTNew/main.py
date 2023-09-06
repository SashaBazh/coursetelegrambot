from mysql.connector import Error
import telebot
import mysql.connector
from datetime import *
import requests
import random
import string
import pyperclip
from telebot import types
from config import *

is_registered = False

bot = telebot.TeleBot("6642921305:AAEL6ZdNP7o7nzHeaQz4haojqnpkWNsbKDE")

host1 = "localhost"
user1 = "root"
password1 = "admin"
port1 = 1111
namePr = "USE Progect"
image1 = "Diedpro.png"
image2 = "Likapro.png"
image3 = "Ivanpro.png"

# Функция для создания базы данных

# Функция получения IP пользователя


def get_user_ip():
    try:
        response = requests.get("https://httpbin.org/ip")
        data = response.json()
        ip_address = data["origin"]
    except requests.exceptions.RequestException:
        ip_address = "Unknown"
    return ip_address


# Обработка команды /start
@bot.message_handler(commands=["start"])
def send_welcome(message):
    bot.send_message(message.chat.id, text=start, parse_mode="Markdown")
    bot.send_message(message.chat.id, text=start2, parse_mode="Markdown")
    msg = bot.send_message(message.chat.id, login, parse_mode="Markdown")
    bot.register_next_step_handler(msg, process_username_step)


# Следующий шаг, получение логина пользователя
def process_username_step(message):
    if (
            message.text.startswith("/start")
            or message.text.startswith("/menu")
            or message.text.startswith("Маркет")
            or message.text.startswith("Личный кабинет")
            or message.text.startswith("Наши проекты")
            or message.text.startswith("Образование")
    ):
        bot.reply_to(
            message,
            "*Сначала полностью начните регистрацию используя команду* /start",
            parse_mode="Markdown",
        )
        return

    # Ваш код для вставки данных в БД
    user_id = message.chat.id

    username = message.text
    # Подключение к серверу MySQL
    cnx = mysql.connector.connect(
        host=host1,
        user=user1,
        password=password1,
        port=port1
    )

    # Создание объекта курсора для выполнения SQL-запросов
    cursor = cnx.cursor()

    # Выбор базы данных
    cursor.execute(namePr)

    # Выполнение SQL-запроса для проверки наличия пользователя
    cursor.execute("SELECT id FROM пользователи WHERE id = %s", (user_id,))
    result = cursor.fetchone()

    # Проверка результата запроса
    if result is not None:
        markup = types.InlineKeyboardMarkup()
        men = types.InlineKeyboardButton("Главное меню", callback_data="men")
        markup.row(men)
        # Пользователь с таким id уже существует
        bot.send_message(
            message.chat.id,
            "*Вы уже зарегистрированы.*",
            reply_markup=markup,
            parse_mode="Markdown")
        cursor.close()
        cnx.close()
        return

    # Выполнение SQL-запросов для вставки данных
    cursor.execute(
        "INSERT INTO пользователи (id, username) VALUES (%s, %s) ON DUPLICATE KEY UPDATE username = %s",
        (user_id, username, username),
    )
    cnx.commit()

    # Закрытие курсора и соединения
    cursor.close()
    cnx.close()

    bot.send_message(message.chat.id, text=email1, parse_mode="Markdown")
    msg = bot.send_message(message.chat.id, email2, parse_mode="Markdown")
    bot.register_next_step_handler(msg, process_email_step)


# Следующий шаг, получение email пользователя
def process_email_step(message):
    if (
            message.text.startswith("/start")
            or message.text.startswith("/menu")
            or message.text.startswith("Маркет")
            or message.text.startswith("Личный кабинет")
            or message.text.startswith("Наши проекты")
            or message.text.startswith("Образование")
    ):
        bot.reply_to(
            message,
            "Нужно вводить данные для регистарции, перезагрузите бота нажав /start",
        )
        return
    email = message.text

    # Подключение к серверу MySQL
    cnx = mysql.connector.connect(
        host=host1,
        user=user1,
        password=password1,
        port=port1
    )

    # Создание объекта курсора для выполнения SQL-запросов
    cursor = cnx.cursor()

    # Выбор базы данных
    cursor.execute(namePr)

    # Выполнение SQL-запросов
    cursor.execute(
        "INSERT IGNORE INTO пользователи (id, email) VALUES (%s, %s)", (
            user_id, email)
    )
    cursor.execute(
        "UPDATE пользователи SET email = %s WHERE id = %s", (email, user_id))
    cnx.commit()

    # Закрытие курсора и соединения
    cursor.close()
    cnx.close()

    msg = bot.send_message(message.chat.id, text=phone, parse_mode="Markdown")
    bot.register_next_step_handler(msg, process_phone_step)


# Следующий шаг, получение телефона пользователя
def process_phone_step(message):
    if (
            message.text.startswith("/start")
            or message.text.startswith("/menu")
            or message.text.startswith("Маркет")
            or message.text.startswith("Личный кабинет")
            or message.text.startswith("Наши проекты")
            or message.text.startswith("Образование")
    ):
        bot.reply_to(
            message,
            "Нужно вводить данные для регистарции, перезагрузите бота нажав /start",
        )
        return
    phone_number = message.text

    # Подключение к серверу MySQL
    cnx = mysql.connector.connect(
        host=host1,
        user=user1,
        password=password1,
        port=port1
    )

    # Создание объекта курсора для выполнения SQL-запросов
    cursor = cnx.cursor()

    # Выбор базы данных
    cursor.execute(namePr)

    cursor.execute(
        "INSERT IGNORE INTO пользователи (id, phone) VALUES (%s, %s)",
        (user_id, phone_number),
    )
    cursor.execute(
        "UPDATE пользователи SET phone = %s WHERE id = %s", (
            phone_number, user_id)
    )
    cnx.commit()

    # Закрытие курсора и соединения
    cursor.close()
    cnx.close()

    msg = bot.send_message(message.chat.id, text=name, parse_mode="Markdown")
    bot.register_next_step_handler(msg, process_full_name_step)


# Следующий шаг, получение полного имени пользователя
def process_full_name_step(message):
    if (
            message.text.startswith("/start")
            or message.text.startswith("/menu")
            or message.text.startswith("Маркет")
            or message.text.startswith("Личный кабинет")
            or message.text.startswith("Наши проекты")
            or message.text.startswith("Образование")
    ):
        bot.reply_to(
            message,
            "Нужно вводить данные для регистарции, перезагрузите бота нажав /start",
        )
        return
    full_name = message.text

    # Подключение к серверу MySQL
    cnx = mysql.connector.connect(
        host=host1,
        user=user1,
        password=password1,
        port=port1
    )

    # Создание объекта курсора для выполнения SQL-запросов
    cursor = cnx.cursor()

    # Выбор базы данных
    cursor.execute(namePr)

    cursor.execute(
        "INSERT IGNORE INTO пользователи (id, full_name) VALUES (%s, %s)",
        (user_id, full_name),
    )
    cursor.execute(
        "UPDATE пользователи SET full_name = %s WHERE id = %s", (
            full_name, user_id)
    )
    cnx.commit()

    # Закрытие курсора и соединения
    cursor.close()
    cnx.close()

    generate_password_button = telebot.types.InlineKeyboardButton(
        "Сгенерировать", callback_data="generate_password"
    )
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.add(generate_password_button)

    msg = bot.send_message(
        message.chat.id, text=password, reply_markup=keyboard, parse_mode="Markdown"
    )
    bot.register_next_step_handler(msg, process_secret_password_step)


# функция которая генерирует рандомный пароль
def generate_random_password():
    length = 8
    characters = string.ascii_letters + string.digits
    passwordd = "".join(random.choice(characters) for _ in range(length))
    return passwordd


passwords = {}  # Словарь для хранения паролей по идентификатору пользователя

# Следующий шаг, получение пароля который ввел пользователь пользователя

secret_passworddd = None


def process_secret_password_step(message):
    if (
            message.text.startswith("/start")
            or message.text.startswith("/menu")
            or message.text.startswith("Маркет")
            or message.text.startswith("Личный кабинет")
            or message.text.startswith("Наши проекты")
            or message.text.startswith("Образование")
    ):
        bot.reply_to(
            message,
            "Нужно вводить данные для регистарции, перезагрузите бота нажав /start",
        )
        return
    global user_id
    user_id = message.chat.id  # Преобразование в строку
    markup = telebot.types.InlineKeyboardMarkup()
    konkye = telebot.types.InlineKeyboardButton("Да", callback_data="yes")
    konkno = telebot.types.InlineKeyboardButton("Нет", callback_data="no")
    markup.row(konkye, konkno)
    secret_password = message.text
    if secret_password == "del":
        # Подключение к базе данных
        cnx = mysql.connector.connect(
            host=host1,
            user=user1,
            password=password1,
            port=port1
        )

        # Создание объекта курсора
        cursor = cnx.cursor()
        cursor.execute(namePr)

        # Выполнение SQL-запроса для удаления всех строк из таблицы
        table_name = "пользователи"
        delete_query = f"DELETE FROM {table_name}"
        cursor.execute(delete_query)

        # Подтверждение изменений в базе данных
        cnx.commit()

        # Закрытие курсора и соединения
        cursor.close()
        cnx.close()
    passwords[user_id] = secret_password

    if secret_password == "/generate":
        secret_password = generate_random_password()

    registration_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ip_address = get_user_ip()

    # Подключение к серверу MySQL
    cnx = mysql.connector.connect(
        host=host1,
        user=user1,
        password=password1,
        port=port1
    )

    # Создание объекта курсора для выполнения SQL-запросов
    cursor = cnx.cursor()

    # Выбор базы данных
    cursor.execute(namePr)

    cursor.execute(
        "INSERT IGNORE INTO пользователи (id, secret_password, registration_date, ip_address) VALUES "
        "(%s, %s, %s, %s)",
        (user_id, secret_password, registration_date, ip_address),
    )
    cursor.execute(
        "UPDATE пользователи SET secret_password = %s, registration_date = %s, "
        "ip_address = %s WHERE id = %s",
        (secret_password, registration_date, ip_address, user_id),
    )
    cnx.commit()

    # Закрытие курсора и соединения
    cursor.close()
    cnx.close()

    # Регистрация завершена, можно выполнить необходимые действия
    bot.send_message(message.chat.id, text=reg, parse_mode="Markdown")
    keyboard = telebot.types.InlineKeyboardMarkup()
    copy_button = telebot.types.InlineKeyboardButton(
        "Скопировать", callback_data="copy_password"
    )
    keyboard.add(copy_button)
    bot.send_message(
        message.chat.id,
        text=sekpas + secret_password,
        reply_markup=keyboard,
        parse_mode="Markdown",
    )

    # Отправка сообщения с кнопкой "Принять участие в конкурсе"
    bot.send_message(
        user_id,
        text=kon,
        reply_markup=markup,
        parse_mode="Markdown")
    global is_registered
    is_registered = True


# Если пользователь нажал "Сгенерировать"
@bot.callback_query_handler(func=lambda call: call.data == "generate_password")
def generate_password_callback(call):
    global user_id
    user_id = str(call.message.chat.id)
    keyboard = types.InlineKeyboardMarkup()
    copy_button = types.InlineKeyboardButton(
        "Скопировать", callback_data="copy_password"
    )
    keyboard.add(copy_button)

    markup = types.InlineKeyboardMarkup()
    konkye2 = types.InlineKeyboardButton("Да", callback_data="yes")
    konkno2 = types.InlineKeyboardButton("Нет", callback_data="no")
    markup.row(konkye2, konkno2)

    secret_password = generate_random_password()
    registration_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ip_address = get_user_ip()
    # Сохраняем пароль в словаре по идентификатору пользователя
    passwords[user_id] = secret_password

    # Подключение к серверу MySQL
    cnx = mysql.connector.connect(
        host=host1,
        user=user1,
        password=password1,
        port=port1
    )

    # Создание объекта курсора для выполнения SQL-запросов
    cursor = cnx.cursor()

    # Выбор базы данных
    cursor.execute(namePr)

    cursor.execute(
        "INSERT IGNORE INTO пользователи (id, secret_password, registration_date, ip_address) VALUES (%s, %s, %s, %s)",
        (user_id, secret_password, registration_date, ip_address),
    )
    cursor.execute(
        "UPDATE пользователи SET secret_password = %s, registration_date = %s, ip_address = %s WHERE id = %s",
        (secret_password, registration_date, ip_address, user_id),
    )
    cnx.commit()

    # Закрытие курсора и соединения
    cursor.close()
    cnx.close()

    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=sekpas2 + secret_password,
        parse_mode="Markdown",
    )

    bot.send_message(
        user_id,
        text=sekpas + secret_password,
        reply_markup=keyboard,
        parse_mode="Markdown",
    )
    bot.send_message(user_id, text=reg, parse_mode="Markdown")

    # Отправка сообщения с кнопкой "Принять участие в конкурсе"
    bot.send_message(
        user_id,
        text=kon,
        reply_markup=markup,
        parse_mode="Markdown")
    global is_registered
    is_registered = True


# Обработка Inline-кнопки "Скопировать"
@bot.callback_query_handler(func=lambda call: call.data == "copy_password")
def copy_password_callback(call):
    user_idd = call.message.chat.id

    if user_idd in passwords:
        generated_password = passwords[user_idd]
        pyperclip.copy(generated_password)
        bot.answer_callback_query(call.id, text="Пароль скопирован!")
    else:
        bot.answer_callback_query(call.id, text="Пароль не найден.")


# Обработка Inline-кнопки "Нет" при участии в конкурс
index = 1
total_images = 3


@bot.callback_query_handler(func=lambda call: call.data == "no")
def no_callback(call):
    bot.send_message(call.message.chat.id, text=otkaz1, parse_mode="Markdown")
    bot.send_message(call.message.chat.id, text=otkaz2, parse_mode="Markdown")
    bot.delete_message(call.message.chat.id, call.message.message_id)

    global index
    global total_images
    index = 1
    markup = types.InlineKeyboardMarkup()
    btn_prev = types.InlineKeyboardButton("⬅️", callback_data="prev_button")
    btn_next = types.InlineKeyboardButton("➡️", callback_data="next_button")
    buy_button = types.InlineKeyboardButton(
        "Купить", callback_data="buy_product")
    btn_index = types.InlineKeyboardButton(
        f"{index}/{total_images}", callback_data="current_index"
    )
    markup.row(btn_prev, btn_index, btn_next)
    markup.row(buy_button)

    file = open(image1, "rb")
    bot.send_photo(
        call.message.chat.id,
        file,
        caption="*Название*: _Digital education_\n"
                "*Описание*: _Описание продукта Digital education_",
        reply_markup=markup,
        parse_mode="Markdown",
    )
    file.close()


# Обработка Inline-кнопки "Да" при участии в конкурсе
@bot.callback_query_handler(func=lambda call: call.data == "yes")
def yes_callback(call):
    user_iddd = call.from_user.id

    send_product_info(user_iddd)
    bot.delete_message(call.message.chat.id, call.message.message_id)


product_name1 = None
index1 = None


# Предоставление продукта который выйграл пользователь


def send_product_info(user_id):
    random.shuffle(
        products
    )  # Перемешиваем список продуктов перед выбором случайного продукта
    product = random.choice(products)
    discount = random.choice(discounts)

    photo_path = product["фото"]
    product_name = product["название"]
    product_description = product["описание"]
    product_price = product["стоимость"]
    discounted_price = product_price - (product_price * discount / 100)

    global product_name1
    global index1
    if product_name == "Digital education":
        index1 = 1
    if product_name == "Флюиды осознанности":
        index1 = 2
    else:
        index1 = 3

    product_name1 = product_name

    message = (
        f"*Название*: _{product_name}_\n\n"
        f"*Описание*: _{product_description}_\n\n"
        f"*Стоимость*: _{product_price} руб._\n"
        f"*Скидка*: _{discount}%_\n\n"
        f"*Цена со скидкой*: _{discounted_price} руб._"
    )

    markup = types.InlineKeyboardMarkup()
    about_button = types.InlineKeyboardButton(
        "Подробнее", callback_data="about_product"
    )
    buy_button = types.InlineKeyboardButton(
        "Приобрести", callback_data=f"buy_product2:{product_name}:{discounted_price}"
    )
    markup.row(about_button, buy_button)

    with open(photo_path, "rb") as photo:
        bot.send_message(
            user_id,
            text=f"*Поздравляем!*",
            parse_mode="Markdown")
        bot.send_message(
            user_id,
            text=f"*Ваш приз*:\n_Скидка: {discount}% на образоватльный продукт_ - *{product_name}*\n",
            parse_mode="Markdown",
        )
        bot.send_photo(
            user_id, photo, caption=message, parse_mode="Markdown", reply_markup=markup
        )


# import webbrowser


@bot.callback_query_handler(func=lambda call: call.data.startswith("about_product"))
def about_product(call):
    global product_name1
    global index1
    if product_name1 == "Digital education" or index1 == 1:
        url = "https://digitaled.info"
    elif product_name1 == "Флюиды осознанности" or index1 == 2:
        url = "http://likas.digitaled.info"
    else:
        url = "http://ivanskornyakov.digitaled.info/"

    bot.send_message(
        call.message.chat.id,
        f"Нажмите [здесь]({url}), чтобы открыть страницу.",
        parse_mode="Markdown",
    )


global_product_name = None
global_discounted_price = None


# Нажатие на кнопку "Приобрести" при показе продукта со скидкой
@bot.callback_query_handler(func=lambda call: call.data.startswith("buy_product2"))
def buy_product_handler(call):
    callback_data = call.data
    product_name, discounted_price = callback_data.split(":")[1:]
    confirm_purchase(call.message, product_name, discounted_price)


# Подтверждение платежа продукта со скидкой
def confirm_purchase(message, product_name, discounted_price):
    markup = types.InlineKeyboardMarkup()
    agree_button = types.InlineKeyboardButton(
        "Согласен", callback_data="agree_purchase"
    )
    decline_button = types.InlineKeyboardButton(
        "Отказаться", callback_data="decline_purchase"
    )
    markup.row(agree_button, decline_button)

    global global_product_name
    global global_discounted_price
    global_product_name = product_name
    global_discounted_price = discounted_price

    bot.send_message(
        message.chat.id,
        f"*Вы совершаете покупку:*\n\n*Название:* {product_name}\n*Цена:* {discounted_price} руб.",
        parse_mode="Markdown",
    )
    bot.send_message(
        message.chat.id,
        "Совершая покупку, вы соглашаетесь с [договором оферты](http://digitaled.info/files/dogovor.docx) и [политикой конфиденциальности](http://digitaled.info/files/policy.docx).",
        reply_markup=markup,
        parse_mode="Markdown",
    )


# Сообщение с сообщением какой товар покупаешь


@bot.callback_query_handler(func=lambda call: call.data == "agree_purchase")
def agree_purchase(call):
    global global_product_name
    global global_discounted_price

    product_name3 = global_product_name
    discounted_price3 = global_discounted_price
    send_invoice(
        call.message, product_name3, discounted_price3
    )  # Передача объекта message в качестве аргумента

    # Подключение к серверу MySQL
    cnx = mysql.connector.connect(
        host=host1,
        user=user1,
        password=password1,
        port=port1
    )

    # Создание объекта курсора для выполнения SQL-запросов
    cursor = cnx.cursor()

    # Выбор базы данных
    cursor.execute(namePr)

    cursor.execute(
        "INSERT IGNORE INTO пользователи (id, course_name, discounted_price) VALUES (%s, %s, %s)",
        (user_id, product_name3, discounted_price3),
    )
    cursor.execute(
        "UPDATE пользователи SET course_name = %s, discounted_price = %s WHERE id = %s",
        (product_name3, discounted_price3, user_id),
    )
    cnx.commit()

    # Закрытие курсора и соединения
    cursor.close()
    cnx.close()


# Кнопка где можно купить продукт со скидкой
def send_invoice(message, product_name, discounted_price):
    global user_id
    bot.send_invoice(
        message.chat.id,
        "Покупка курса",
        f"{product_name}",
        "invoice",
        "284685063:TEST:MjAxYWYxZGQyNWE5",
        "USD",
        [types.LabeledPrice(f"{product_name}",
                            int(float(discounted_price) * 100))],
    )


# Сообщение если ты отказался от покупки
@bot.callback_query_handler(func=lambda call: call.data == "decline_purchase")
def decline_purchase_handler(call):
    markup = types.InlineKeyboardMarkup()
    men = types.InlineKeyboardButton("Главное меню", callback_data="men")
    markup.row(men)
    bot.send_message(
        call.message.chat.id,
        "*❌Вы отказались от покупки.*",
        parse_mode="Markdown",
        reply_markup=markup,
    )


def men(message):
    global is_registered

    if not is_registered:
        keyboard = types.InlineKeyboardMarkup()
        start_button = types.InlineKeyboardButton(
            "Начать регистрацию заново", callback_data="restart_registration"
        )
        keyboard.add(start_button)
        # bot.reply_to(message, "Сначала зарегистрируйтесь")
        bot.send_message(
            message.chat.id,
            text="*Сначала полностью зарегистрируйтесь* нажав /start",
            parse_mode="Markdown",
        )

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    education_button = types.KeyboardButton("Образование")
    market = types.KeyboardButton("Маркет")
    our_projects_button = types.KeyboardButton("Наши проекты")
    personal_cabinet_button = types.KeyboardButton("Личный кабинет")
    markup.add(
        education_button,
        market,
        our_projects_button,
        personal_cabinet_button)

    bot.send_message(
        message.chat.id,
        "👋🏻*Добро пожаловать в главное меню!*",
        reply_markup=markup,
        parse_mode="Markdown",
    )


# Обработка команды /start
@bot.message_handler(commands=["menu"])
def create_main_menu_markup(message):
    print("qqqqq")
    global is_registered
    if not is_registered:
        keyboard = types.InlineKeyboardMarkup()
        print("lllll")
        start_button = types.InlineKeyboardButton(
            "Начать регистрацию заново", callback_data="restart_registration"
        )
        keyboard.add(start_button)
        # bot.reply_to(message, "Сначала зарегистрируйтесь")
        bot.send_message(
            message.chat.id,
            text="*Сначала полностью зарегистрируйтесь* нажав /start",
            parse_mode="Markdown",
        )

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    education_button = types.KeyboardButton("Образование")
    market = types.KeyboardButton("Маркет")
    our_projects_button = types.KeyboardButton("Наши проекты")
    personal_cabinet_button = types.KeyboardButton("Личный кабинет")
    markup.add(
        education_button,
        market,
        our_projects_button,
        personal_cabinet_button)

    bot.send_message(
        message.chat.id,
        "👋🏻 *Добро пожаловать в главное меню!*",
        reply_markup=markup,
        parse_mode="Markdown",
    )


# переменные для слайдера
# index1 = 1
# total_images = 3


# Обработка нажатия на кнопку Маркет
@bot.message_handler(func=lambda message: message.text == "Маркет")
def market(message):
    global index1
    index1 = 1
    markup = types.InlineKeyboardMarkup()
    btn_prev = types.InlineKeyboardButton("⬅️", callback_data="prev_button1")
    btn_next = types.InlineKeyboardButton("➡️", callback_data="next_button1")
    buy_button = types.InlineKeyboardButton(
        "Приобрести", callback_data="buy_product")
    about_button = types.InlineKeyboardButton(
        "Подробнее", callback_data="about_product"
    )
    btn_index = types.InlineKeyboardButton(
        f"{index1}/{total_images}", callback_data="current_index"
    )
    markup.row(btn_prev, btn_index, btn_next)
    markup.row(about_button, buy_button)

    file = open(image1, "rb")
    bot.send_photo(
        message.chat.id,
        file,
        caption="*Название*: _Digital education_\n*Описание*: _Описание продукта Digital education_\n\n💸*Стоимость*: 100",
        reply_markup=markup,
        parse_mode="Markdown",
    )
    file.close()


# отслеживание индексов предыдущей кнопки
def prev_button1(message):
    global index1
    index1 -= 1
    if index1 < 1:
        index1 = total_images
    change_image1(message, index1)


# отслеживание индексов следующей кнопки
def next_button1(message):
    global index1
    index1 += 1
    if index1 > total_images:
        index1 = 1
    change_image1(message, index1)


# слайдер с товарами
def change_image1(message, index1):
    markup = types.InlineKeyboardMarkup()
    btn_prev = types.InlineKeyboardButton("⬅️", callback_data="prev_button1")
    btn_next = types.InlineKeyboardButton("➡️", callback_data="next_button1")
    buy_button = types.InlineKeyboardButton(
        "Приобрести", callback_data="buy_product")
    about_button = types.InlineKeyboardButton(
        "Подробнее", callback_data="about_product"
    )
    btn_index = types.InlineKeyboardButton(
        f"{index1}/{total_images}", callback_data="current_index"
    )
    markup.row(btn_prev, btn_index, btn_next)
    markup.row(about_button, buy_button)

    caption1 = image_captions2[index1]

    if index1 == 1:
        with open(image1, "rb") as file:
            bot.edit_message_media(
                chat_id=message.chat.id,
                message_id=message.id,
                media=types.InputMediaPhoto(file),
                reply_markup=markup,
            )
            bot.edit_message_caption(
                chat_id=message.chat.id,
                message_id=message.id,
                caption=caption1,
                reply_markup=markup,
                parse_mode="Markdown",
            )
    elif index1 == 2:
        with open(image2, "rb") as file:
            bot.edit_message_media(
                chat_id=message.chat.id,
                message_id=message.id,
                media=types.InputMediaPhoto(file),
                reply_markup=markup,
            )
            bot.edit_message_caption(
                chat_id=message.chat.id,
                message_id=message.id,
                caption=caption1,
                reply_markup=markup,
                parse_mode="Markdown",
            )
    elif index1 == 3:
        with open(image3, "rb") as file:
            bot.edit_message_media(
                chat_id=message.chat.id,
                message_id=message.id,
                media=types.InputMediaPhoto(file),
                reply_markup=markup,
            )
            bot.edit_message_caption(
                chat_id=message.chat.id,
                message_id=message.id,
                caption=caption1,
                reply_markup=markup,
                parse_mode="Markdown",
            )


# Нажатие на кнопку "Приобрести" при показе продукта без скидки
def buy_product(message):
    global user_id

    keyboard = types.InlineKeyboardMarkup()
    agree_button = types.InlineKeyboardButton(
        "Согласен", callback_data="agree")
    disagree_button = types.InlineKeyboardButton(
        "Отказаться", callback_data="disagree")
    keyboard.add(agree_button, disagree_button)
    bot.send_message(
        message.chat.id,
        "Совершая покупку, вы соглашаетесь с [договором оферты](http://digitaled.info/files/dogovor.docx) и [политикой конфиденциальности](http://digitaled.info/files/policy.docx).",
        reply_markup=keyboard,
        parse_mode="Markdown",
    )


def agree(message):
    user_id = message.chat.id
    product = None
    if index1 == 1:
        product = "Digital education"
    if index1 == 2:
        product = "Флюиды осознанности"
    if index1 == 3:
        product = "Иван Скорняков"
    price = image_prices[index1]
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    bot.send_invoice(
        message.chat.id,
        "Покупка курса",
        f"{product}",
        "invoice",
        "284685063:TEST:MjAxYWYxZGQyNWE5",
        "USD",
        [types.LabeledPrice(f"{product}", price * 100)],
    )
    insert_purchase(
        product, price, user_id, date
    )  # Передача user_id в функцию insert_purchase


def disagree(message):
    markup = types.InlineKeyboardMarkup()
    men = types.InlineKeyboardButton("Главное меню", callback_data="men")
    markup.row(men)
    bot.send_message(
        message.chat.id,
        "*❌Вы отказались от покупки.*",
        parse_mode="Markdown",
        reply_markup=markup,
    )


# Добавление в бд купленного товара без скидки----------------------------


def insert_purchase(product, price, user_id, date):
    # Подключение к базе данных MySQL
    conn = mysql.connector.connect(
        host=host1,
        user=user1,
        password=password1,
        port=port1
    )
    cursor = conn.cursor()

    # Выбор базы данных
    cursor.execute(namePr)

    # Получение текущих значений столбцов product и price для пользователя
    cursor.execute(
        "SELECT product, price, contest_participation_date FROM пользователи WHERE id = %s",
        (user_id,),
    )
    result = (
        cursor.fetchone()
    )  # возвращает кортеж (product, price, contest_participation_date) или None
    if result is not None:
        current_product, current_price, current_date = result
    else:
        current_product, current_price, current_date = "", "", ""

    # Добавление новых значений к текущим
    new_product = current_product + ", " + product if current_product else product
    new_price = str(current_price) + ", " + \
        str(price) if current_price else str(price)
    new_date = str(current_date) + ", " + \
        str(date) if current_date else str(date)

    # Обновление значений столбцов product и price для пользователя
    cursor.execute(
        "UPDATE пользователи SET product = %s, price = %s, contest_participation_date = %s WHERE id = %s",
        (new_product, new_price, new_date, user_id),
    )
    conn.commit()
    conn.close()


# кал беки
@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    if callback.data == "prev_button1":
        prev_button1(callback.message)
    if callback.data == "next_button1":
        next_button1(callback.message)
    if callback.data == "prev_button":
        prev_button(callback.message)
    if callback.data == "next_button":
        next_button(callback.message)
    if callback.data == "buy_product":
        buy_product(callback.message)
    if callback.data == "agree":
        agree(callback.message)
    if callback.data == "disagree":
        disagree(callback.message)
    if callback.data == "men":
        men(callback.message)
    if callback.data == "contacts":
        contacts(callback.message)
    if callback.data == "subscriptions":
        subscriptions(callback.message)
    if callback.data == "psw":
        psw(callback.message)
    if callback.data == "prev_button4":
        prev_button4(callback.message)
    if callback.data == "next_button4":
        next_button4(callback.message)
    if callback.data == "prev_buttonsl":
        prev_buttonsl(callback.message)
    if callback.data == "next_buttonsl":
        next_buttonsl(callback.message)
    if callback.data == "prev_buttonst":
        prev_buttonst(callback.message)
    if callback.data == "next_buttonst":
        next_buttonst(callback.message)
    if callback.data == "one":
        one(callback.message)
    if callback.data == "week":
        week(callback.message)
    if callback.data == "month":
        month(callback.message)
    if callback.data == "oll":
        oll(callback.message)
    if callback.data == "one1":
        one1(callback.message)
    if callback.data == "week1":
        week1(callback.message)
    if callback.data == "month1":
        month1(callback.message)
    if callback.data == "oll1":
        oll1(callback.message)


@bot.message_handler(func=lambda message: message.text == "Личный кабинет")
def handle_personal_cabinet(message):
    user_id = message.chat.id
    conn = None
    cursor = None
    try:
        conn = mysql.connector.connect(
            host=host1,
            user=user1,
            password=password1,
            port=port1
        )
        cursor = conn.cursor()

        # Выбор базы данных
        cursor.execute(namePr)

        # Получаем данные пользователя из базы данных
        cursor.execute("SELECT * FROM пользователи WHERE id = %s", (user_id,))
        user_data = cursor.fetchone()

        if user_data is None:
            bot.send_message(message.chat.id, "Вы еще не зарегистрированы.")
            return

        # Разбираем данные пользователя
        username = user_data[1]
        email = user_data[2]
        phone = user_data[3]
        full_name = user_data[4]
        registration = user_data[6]

        # Формируем информацию о пользователе
        personal_info = (
            f"*Личный кабинет*:\n\n"
            f"*Логин*: _{username}_\n"
            f"*Имя*: _{full_name}_\n"
            f"*Email*: _{email}_\n"
            f"*Дата регистрации*: _{registration}_\n"
            f"*Контактный телефон*: _{phone}_\n"
        )

        # Отправляем сообщение пользователю
        markup = types.InlineKeyboardMarkup()
        subscriptions = types.InlineKeyboardButton(
            "Подписки", callback_data="subscriptions"
        )
        contacts = types.InlineKeyboardButton(
            "Контакты", callback_data="contacts")
        psw = types.InlineKeyboardButton("Пароль", callback_data="psw")

        markup.row(subscriptions, contacts)
        markup.row(psw)

        bot.send_message(
            message.chat.id, personal_info, reply_markup=markup, parse_mode="Markdown"
        )

    except Error as e:
        # Обработка ошибок при подключении к базе данных
        print(f"Ошибка при подключении к базе данных: {e}")
        bot.send_message(
            message.chat.id, "Произошла ошибка при получении данных из базы данных."
        )

    finally:
        # Закрытие соединения с базой данных
        if conn is not None and conn.is_connected():
            cursor.close()
            conn.close()


def contacts(message):
    bot.send_message(
        message.chat.id,
        "*Email*: hello@digitaled.info\n*Support*: support@digitaled.info\n*Site*: Digitaled.info",
        parse_mode="Markdown",
    )


def subscriptions(message):
    user_id = message.chat.id

    conn = mysql.connector.connect(
        host=host1,
        user=user1,
        password=password1,
        port=port1
    )
    cursor = conn.cursor()

    # Выбор базы данных
    cursor.execute(namePr)

    # Получаем данные пользователя из базы данных
    cursor.execute("SELECT * FROM пользователи WHERE id = %s", (user_id,))
    user_data = cursor.fetchone()

    if user_data is None:
        bot.send_message(message.chat.id, "У вас нету подписок")
        return

    # Разбираем данные пользователя
    data = user_data[11]
    sub = user_data[12]
    price = user_data[13]

    # Формируем информацию о пользователе
    personal_info = (
        f"*Ваши подписки*:\n\n"
        f"*Название*: _{sub}_\n"
        f"*Дата оформления*: _{data}_\n\n"
        f"*Мои оплаты*: _{price}_\n\n"
        f"*Дата платежа*: _{data}_\n"
    )

    bot.send_message(message.chat.id, personal_info, parse_mode="Markdown")

    conn.close()


passwords2 = (
    {}
)  # Словарь для хранения паролей по идентификатору пользователяpasswords = {}  # Словарь для хранени


def psw(message):
    user_id = message.chat.id

    conn = mysql.connector.connect(
        host=host1,
        user=user1,
        password=password1,
        port=port1
    )
    cursor = conn.cursor()
    cursor.execute(namePr)

    # Получаем данные пользователя из базы данных
    cursor.execute("SELECT * FROM пользователи WHERE id = %s", (user_id,))
    user_data = cursor.fetchone()

    if user_data is None:
        bot.send_message(message.chat.id, "Вы еще не зарегистрированы.")
        return

    psw_value = user_data[5]
    pyperclip.copy(psw_value)
    keyboard = types.InlineKeyboardMarkup()
    copy_button = types.InlineKeyboardButton(
        "Скопировать", callback_data="copy_passw")
    keyboard.add(copy_button)
    bot.send_message(
        message.chat.id,
        text=sekpas + " " + psw_value,
        reply_markup=keyboard,
        parse_mode="Markdown",
    )
    passwords2[user_id] = psw_value

    conn.close()


# Обработка нажатия на кнопку Образование
@bot.message_handler(func=lambda message: message.text == "Образование")
def handle_education(message):
    markup = types.InlineKeyboardMarkup()
    channel_button = types.InlineKeyboardButton(
        "Канал", url="https://t.me/+I2GA5vUkLmc2MTNi"
    )
    chat_button = types.InlineKeyboardButton(
        "Чат", url="https://t.me/+zIYKF6WCdekzY2My"
    )

    bot.send_message(message.chat.id, "*Образование:*", parse_mode="Markdown")

    global index
    index = 1
    btn_prev = types.InlineKeyboardButton("⬅️", callback_data="prev_button")
    btn_next = types.InlineKeyboardButton("➡️", callback_data="next_button")
    btn_index = types.InlineKeyboardButton(
        f"{index}/{total_images}", callback_data="current_index"
    )
    markup.row(btn_prev, btn_index, btn_next)
    markup.row(channel_button, chat_button)

    file = open(image1, "rb")
    bot.send_photo(
        message.chat.id,
        file,
        caption="*Название*: _Digital education_\n*Описание*: _Описание продукта Digital education_",
        reply_markup=markup,
        parse_mode="Markdown",
    )
    file.close()


# отслеживание индексов предыдущей кнопки
def prev_button(message):
    global index
    index -= 1
    if index < 1:
        index = total_images
    change_image(message, index)


# отслеживание индексов следующей кнопки
def next_button(message):
    global index
    index += 1
    if index > total_images:
        index = 1
    change_image(message, index)


# слайдер с товарами
def change_image(message, index):
    markup = types.InlineKeyboardMarkup()
    btn_prev = types.InlineKeyboardButton("⬅️", callback_data="prev_button")
    btn_next = types.InlineKeyboardButton("➡️", callback_data="next_button")
    channel_button = types.InlineKeyboardButton(
        "Канал", url="https://t.me/+I2GA5vUkLmc2MTNi"
    )
    chat_button = types.InlineKeyboardButton(
        "Чат", url="https://t.me/+zIYKF6WCdekzY2My"
    )
    btn_index = types.InlineKeyboardButton(
        f"{index}/{total_images}", callback_data="current_index"
    )
    markup.row(btn_prev, btn_index, btn_next)
    markup.row(channel_button, chat_button)

    caption = image_captions[index]

    if index == 1:
        with open(image1, "rb") as file:
            bot.edit_message_media(
                chat_id=message.chat.id,
                message_id=message.id,
                media=types.InputMediaPhoto(file),
                reply_markup=markup,
            )
            bot.edit_message_caption(
                chat_id=message.chat.id,
                message_id=message.id,
                caption=caption,
                reply_markup=markup,
                parse_mode="Markdown",
            )
    elif index == 2:
        with open(image2, "rb") as file:
            bot.edit_message_media(
                chat_id=message.chat.id,
                message_id=message.id,
                media=types.InputMediaPhoto(file),
                reply_markup=markup,
            )
            bot.edit_message_caption(
                chat_id=message.chat.id,
                message_id=message.id,
                caption=caption,
                reply_markup=markup,
                parse_mode="Markdown",
            )
    elif index == 3:
        with open(image3, "rb") as file:
            bot.edit_message_media(
                chat_id=message.chat.id,
                message_id=message.id,
                media=types.InputMediaPhoto(file),
                reply_markup=markup,
            )
            bot.edit_message_caption(
                chat_id=message.chat.id,
                message_id=message.id,
                caption=caption,
                reply_markup=markup,
                parse_mode="Markdown",
            )


# Нажатие на кнопку "Приобрести" при показе продукта без скидки


# Обработка нажатия на кнопку Наши проекты
@bot.message_handler(func=lambda message: message.text == "Наши проекты")
def handle_our_projects(message):
    markup = types.InlineKeyboardMarkup()
    video = types.InlineKeyboardButton(
        "Видео студия", url="https://instagram.com/fresh.ms?igshid=NTc4MTIwNjQ2YQ=="
    )
    brain = types.InlineKeyboardButton(
        "Brain University ", url="https://Brainuniversity.ru"
    )

    markup.row(video)
    markup.row(brain)

    bot.send_message(
        message.chat.id, "*Наши проекты*:", reply_markup=markup, parse_mode="Markdown"
    )


# Обработка нажатия кнопки "Назад"
@bot.callback_query_handler(func=lambda call: call.data == "back")
def handle_back(callback_query):
    markup = create_main_menu_markup()
    bot.edit_message_text(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        text="Добро пожаловать в главное меню!",
        reply_markup=markup,
    )


# Админка---------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------

@bot.message_handler(commands=["adminka"])
def admin_start(message):
    bot.send_message(
        message.chat.id,
        "*Добро пожаловать в бот администратора Digital Education*:",
        parse_mode="Markdown",
    )
    bot.send_message(message.chat.id, "_Введите свой пароль_:",
                     parse_mode="Markdown")
    bot.register_next_step_handler(
        message, pass_adm
    )  # Передаем объект message, а не строку


def pass_adm(message):
    pass_adm = message.text
    user_id = message.from_user.id  # Добавляем получение user_id из message

    conn = mysql.connector.connect(
        host=host1, user=user1, password=password1, port=port1
    )
    cursor = conn.cursor()
    cursor.execute(namePr)
    cursor.execute(
        "UPDATE пользователи SET pass_adm = %s WHERE id = %s", (
            pass_adm, user_id)
    )
    conn.commit()
    conn.close()
    print(pass_adm)
    bot.send_message(
        message.chat.id,
        "*Поздравляем, вы успешно авторизовались в системе!*",
        parse_mode="Markdown",
    )
    bot.send_message(
        message.chat.id, "*Меню админа /adminmenu*", parse_mode="Markdown")


@bot.message_handler(commands=["adminmenu"])
def adminmen(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    prog = types.KeyboardButton("Проекты")
    Stat = types.KeyboardButton("Статистика")
    cab = types.KeyboardButton("Личный кабинет")
    markup.add(prog, Stat, cab)

    bot.send_message(
        message.chat.id,
        "👋🏻 *Добро пожаловать в главное меню админа!*",
        reply_markup=markup,
        parse_mode="Markdown",
    )


indexsl = 1
captionsl = ""
index4 = 1
total_images4 = 3


@bot.message_handler(func=lambda message: message.text == "Проекты")
def progect4(message):

    bot.send_message(
        message.chat.id, "*Обобщенная информация:*", parse_mode="Markdown")
    global index4
    index4 = 1
    markup = types.InlineKeyboardMarkup()
    btn_prev4 = types.InlineKeyboardButton("⬅️", callback_data="prev_button4")
    btn_next4 = types.InlineKeyboardButton("➡️", callback_data="next_button4")
    btn_index4 = types.InlineKeyboardButton(
        f"{index4}/{total_images4}", callback_data="current_index4"
    )
    markup.row(btn_prev4, btn_index4, btn_next4)

    file = open(image1, "rb")
    bot.send_photo(
        message.chat.id,
        file,
        caption="*Название*: _Digital education_\n*Описание*: _Описание продукта Digital education_\n*Стоимость*: 100",
        reply_markup=markup,
        parse_mode="Markdown",
    )
    file.close()

    global indexsl
    global captionsl
    indexsl = 1

    captionsl = "*Ключевая по ученикам*\n\n*Учеников:*\n*Новых учеников:*\n*Переходов:*\n*Просмотров:*\n*Продаж:*"
    markupsl = types.InlineKeyboardMarkup()
    btn_prevsl = types.InlineKeyboardButton(
        "⬅️", callback_data="prev_buttonsl")
    btn_nextsl = types.InlineKeyboardButton(
        "➡️", callback_data="next_buttonsl")

    one = types.InlineKeyboardButton("Один день", callback_data="one")
    week = types.InlineKeyboardButton("Неделя", callback_data="week")
    month = types.InlineKeyboardButton("Месяц", callback_data="month")
    oll = types.InlineKeyboardButton("Все время", callback_data="oll")
    podr = types.InlineKeyboardButton("Подробнее", callback_data="podr")

    btn_indexsl = types.InlineKeyboardButton(
        f"{indexsl}/{4}", callback_data="current_indexsl"
    )

    markupsl.row(btn_prevsl, btn_indexsl, btn_nextsl)
    markupsl.row(one, week)
    markupsl.row(month, oll)
    markupsl.row(podr)

    bot.send_message(
        message.chat.id, captionsl, reply_markup=markupsl, parse_mode="Markdown"
    )


def prev_button4(message):
    global index4
    index4 -= 1
    if index4 < 1:
        index4 = total_images4
    change_image4(message, index4)


def next_button4(message):
    global index4
    index4 += 1
    if index4 > total_images4:
        index4 = 1
    change_image4(message, index4)


def change_image4(message, index4):
    markup = types.InlineKeyboardMarkup()
    btn_prev4 = types.InlineKeyboardButton("⬅️", callback_data="prev_button4")
    btn_next4 = types.InlineKeyboardButton("➡️", callback_data="next_button4")
    btn_index4 = types.InlineKeyboardButton(
        f"{index4}/{total_images4}", callback_data="current_index4"
    )
    markup.row(btn_prev4, btn_index4, btn_next4)

    caption4 = image_captions2[index4]

    if index4 == 1:
        with open(image1, "rb") as file:
            bot.edit_message_media(
                chat_id=message.chat.id,
                message_id=message.id,
                media=types.InputMediaPhoto(file),
                reply_markup=markup,
            )
            bot.edit_message_caption(
                chat_id=message.chat.id,
                message_id=message.id,
                caption=caption4,
                reply_markup=markup,
                parse_mode="Markdown",
            )
    elif index4 == 2:
        with open(image2, "rb") as file:
            bot.edit_message_media(
                chat_id=message.chat.id,
                message_id=message.id,
                media=types.InputMediaPhoto(file),
                reply_markup=markup,
            )
            bot.edit_message_caption(
                chat_id=message.chat.id,
                message_id=message.id,
                caption=caption4,
                reply_markup=markup,
                parse_mode="Markdown",
            )
    elif index4 == 3:
        with open(image3, "rb") as file:
            bot.edit_message_media(
                chat_id=message.chat.id,
                message_id=message.id,
                media=types.InputMediaPhoto(file),
                reply_markup=markup,
            )
            bot.edit_message_caption(
                chat_id=message.chat.id,
                message_id=message.id,
                caption=caption4,
                reply_markup=markup,
                parse_mode="Markdown",
            )


def prev_buttonsl(message):
    global indexsl
    indexsl -= 1
    if indexsl < 1:
        indexsl = 4
    change_textsl(message, indexsl)


def next_buttonsl(message):
    global indexsl
    indexsl += 1
    if indexsl > 4:
        indexsl = 1
    change_textsl(message, indexsl)


def change_textsl(message, indexsl):
    global captionsl

    conn = mysql.connector.connect(
        host=host1,
        user=user1,
        password=password1,
        port=port1
    )

    cursor = conn.cursor()
    cursor.execute(namePr)

    # получить количество учеников
    cursor.execute("SELECT COUNT(*) FROM пользователи")
    count = cursor.fetchone()[0]

    # Получение текущей даты и времени
    current_datetime = datetime.now()
    # Вычисление даты и времени, которая была 24 часа назад
    past_datetime = current_datetime - timedelta(hours=24)
    # Преобразование даты и времени в формат, подходящий для SQL-запроса
    past_datetime_str = past_datetime.strftime("%Y-%m-%d %H:%M:%S")
    # Выполнение запроса на подсчет новых учеников
    query = "SELECT COUNT(*) FROM пользователи WHERE registration_date >= %s"
    cursor.execute(query, (past_datetime_str,))
    # Получение результата запроса
    count24 = cursor.fetchone()[0]

    cursor.execute(
        "SELECT SUM(CEIL(CHAR_LENGTH(price) / 4.5)) FROM пользователи WHERE price != ''")
    countprice = cursor.fetchone()[0]

    cursor.execute("SELECT price FROM пользователи WHERE price != ''")
    result = cursor.fetchall()  # Получение всех результатов
    prices = [row[0] for row in result]  # Получение значений столбца "price"
    viruchka = 0
    for item in prices:
        nums = item.split(',')
        nums = [int(num.strip()) for num in nums]
        viruchka += sum(nums)

    cursor.execute(
        "SELECT COUNT(*) FROM пользователи WHERE discounted_price != ''")
    discount = cursor.fetchone()[0]

    cursor.execute(
        "SELECT price FROM пользователи WHERE discounted_price != ''")
    result = cursor.fetchall()  # Получение всех результатов
    # Получение значений столбца "price"
    pricessale = [row[0] for row in result]
    viruchkasale = 0
    for item in pricessale:
        nums = item.split(',')
        nums = [int(num.strip()) for num in nums]
        viruchkasale += sum(nums)

    # закрываем соединение
    conn.commit()
    conn.close()

    if indexsl == 1:
        captionsl = f"*Ключевая по ученикам*\n\n*Учеников: {count}*\n*Новых учеников: {count24}*\n*Переходов: {count}*\n*Просмотров: {count}*\n*Продаж: {countprice}*"
    elif indexsl == 2:
        captionsl = f"*Финансы*\n\n*Оплат: {countprice}*\n*Выручка: {viruchka}*\n*Сумма скидок: {discount}*\n*Подарено скидок на сумму: {viruchkasale}*"
    elif indexsl == 3:
        captionsl = f"*Переходы*\n\n*Посещений сайта: {count}*\n*Переходов в бота с сайта: {0}*\n*Другие источники: {0}*"
    elif indexsl == 4:
        captionsl = f"*Подписки*\n\n*Активных подписок: {countprice} *\n*Отменено подписок: {0}*"

    markupsl = types.InlineKeyboardMarkup()
    btn_prevsl = types.InlineKeyboardButton(
        "⬅️", callback_data="prev_buttonsl")
    btn_nextsl = types.InlineKeyboardButton(
        "➡️", callback_data="next_buttonsl")
    one = types.InlineKeyboardButton("1 день", callback_data="one1")
    week = types.InlineKeyboardButton("7 дней", callback_data="week2")
    month = types.InlineKeyboardButton("Месяц", callback_data="month3")
    oll = types.InlineKeyboardButton("Все время", callback_data="oll4")
    podr = types.InlineKeyboardButton("Подробнее", callback_data="podr")
    btn_indexsl = types.InlineKeyboardButton(
        f"{indexsl}/{4}", callback_data="current_indexsl"
    )
    markupsl.row(btn_prevsl, btn_indexsl, btn_nextsl)
    markupsl.row(one, week)
    markupsl.row(month, oll)
    markupsl.row(podr)

    if indexsl == 1:
        bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=message.id,
            text=captionsl,
            reply_markup=markupsl,
            parse_mode="Markdown",
        )
    elif indexsl == 2:
        bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=message.id,
            text=captionsl,
            reply_markup=markupsl,
            parse_mode="Markdown",
        )
    elif indexsl == 3:
        bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=message.id,
            text=captionsl,
            reply_markup=markupsl,
            parse_mode="Markdown",
        )
    elif indexsl == 4:
        bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=message.id,
            text=captionsl,
            reply_markup=markupsl,
            parse_mode="Markdown",
        )


def one1(message):
    global captionsl
    global indexsl

    conn = mysql.connector.connect(
        host=host1,
        user=user1,
        password=password1,
        port=port1
    )

    cursor = conn.cursor()
    cursor.execute(namePr)

    # Вычисление даты начала и конца 7-дневного периода
    today = datetime.now().date()
    one = today - timedelta(days=1)

    # получить количество учеников
    cursor.execute(
        f"SELECT COUNT(*) FROM пользователи WHERE registration_date >= '{one}'")
    count = cursor.fetchone()[0]

    # Получение текущей даты и времени
    current_datetime = datetime.now()
    # Вычисление даты и времени, которая была 24 часа назад
    past_datetime = current_datetime - timedelta(hours=24)
    # Преобразование даты и времени в формат, подходящий для SQL-запроса
    past_datetime_str = past_datetime.strftime("%Y-%m-%d %H:%M:%S")
    # Выполнение запроса на подсчет новых учеников
    query = f"SELECT COUNT(*) FROM пользователи WHERE registration_date >= %s AND registration_date >= '{one}'"
    cursor.execute(query, (past_datetime_str,))
    # Получение результата запроса
    count24 = cursor.fetchone()[0]

    cursor.execute(
        f"SELECT SUM(CEIL(CHAR_LENGTH(price) / 4.5)) FROM пользователи WHERE price != '' AND registration_date >= '{one}'")
    countprice = cursor.fetchone()[0]

    cursor.execute(
        f"SELECT price FROM пользователи WHERE price != '' AND registration_date >= '{one}'")
    result = cursor.fetchall()  # Получение всех результатов
    prices = [row[0] for row in result]  # Получение значений столбца "price"
    viruchka = 0
    for item in prices:
        nums = item.split(',')
        nums = [int(num.strip()) for num in nums]
        viruchka += sum(nums)

    cursor.execute(
        f"SELECT COUNT(*) FROM пользователи WHERE discounted_price != '' AND registration_date >= '{one}'")
    discount = cursor.fetchone()[0]

    cursor.execute(
        f"SELECT price FROM пользователи WHERE discounted_price != '' AND registration_date >= '{one}'")
    result = cursor.fetchall()  # Получение всех результатов
    # Получение значений столбца "price"
    pricessale = [row[0] for row in result]
    viruchkasale = 0
    for item in pricessale:
        nums = item.split(',')
        nums = [int(num.strip()) for num in nums]
        viruchkasale += sum(nums)

    # закрываем соединение
    conn.commit()
    conn.close()

    if indexsl == 1:
        captionsl = f"*Ключевая по ученикам*\n\n*Учеников: {count}*\n*Новых учеников: {count24}*\n*Переходов: {count}*\n*Просмотров: {count}*\n*Продаж: {countprice}*"
    elif indexsl == 2:
        captionsl = f"*Финансы*\n\n*Оплат: {countprice}*\n*Выручка: {viruchka}*\n*Сумма скидок: {discount}*\n*Подарено скидок на сумму: {viruchkasale}*"
    elif indexsl == 3:
        captionsl = f"*Переходы*\n\n*Посещений сайта: {count}*\n*Переходов в бота с сайта: {0}*\n*Другие источники: {0}*"
    elif indexsl == 4:
        captionsl = f"*Подписки*\n\n*Активных подписок: {countprice} *\n*Отменено подписок: {0}*"

    markupsl = types.InlineKeyboardMarkup()
    btn_prevsl = types.InlineKeyboardButton(
        "⬅️", callback_data="prev_buttonsl")
    btn_nextsl = types.InlineKeyboardButton(
        "➡️", callback_data="next_buttonsl")
    one = types.InlineKeyboardButton("1 день", callback_data="one1")
    week = types.InlineKeyboardButton("7 дней", callback_data="week2")
    month = types.InlineKeyboardButton("Месяц", callback_data="month3")
    oll = types.InlineKeyboardButton("Все время", callback_data="oll4")
    podr = types.InlineKeyboardButton("Подробнее", callback_data="podr")
    btn_indexsl = types.InlineKeyboardButton(
        f"{indexsl}/{4}", callback_data="current_indexsl"
    )
    markupsl.row(btn_prevsl, btn_indexsl, btn_nextsl)
    markupsl.row(one, week)
    markupsl.row(month, oll)
    markupsl.row(podr)

    if indexst in [1, 2, 3, 4]:
        bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=message.id,
            text=captionsl,
            reply_markup=markupsl,
            parse_mode="Markdown",
        )


def week1(message):
    global captionsl
    global indexsl

    conn = mysql.connector.connect(
        host=host1,
        user=user1,
        password=password1,
        port=port1
    )

    cursor = conn.cursor()
    cursor.execute(namePr)

    # Вычисление даты начала и конца 7-дневного периода
    today = datetime.now().date()
    seven = today - timedelta(days=1)

    # получить количество учеников
    cursor.execute(
        f"SELECT COUNT(*) FROM пользователи WHERE registration_date >= '{seven}'")
    count = cursor.fetchone()[0]

    # Получение текущей даты и времени
    current_datetime = datetime.now()
    # Вычисление даты и времени, которая была 24 часа назад
    past_datetime = current_datetime - timedelta(hours=24)
    # Преобразование даты и времени в формат, подходящий для SQL-запроса
    past_datetime_str = past_datetime.strftime("%Y-%m-%d %H:%M:%S")
    # Выполнение запроса на подсчет новых учеников
    query = f"SELECT COUNT(*) FROM пользователи WHERE registration_date >= %s AND registration_date >= '{seven}'"
    cursor.execute(query, (past_datetime_str,))
    # Получение результата запроса
    count24 = cursor.fetchone()[0]

    cursor.execute(
        f"SELECT SUM(CEIL(CHAR_LENGTH(price) / 4.5)) FROM пользователи WHERE price != '' AND registration_date >= '{seven}'")
    countprice = cursor.fetchone()[0]

    cursor.execute(
        f"SELECT price FROM пользователи WHERE price != '' AND registration_date >= '{seven}'")
    result = cursor.fetchall()  # Получение всех результатов
    prices = [row[0] for row in result]  # Получение значений столбца "price"
    viruchka = 0
    for item in prices:
        nums = item.split(',')
        nums = [int(num.strip()) for num in nums]
        viruchka += sum(nums)

    cursor.execute(
        f"SELECT COUNT(*) FROM пользователи WHERE discounted_price != '' AND registration_date >= '{seven}'")
    discount = cursor.fetchone()[0]

    cursor.execute(
        f"SELECT price FROM пользователи WHERE discounted_price != '' AND registration_date >= '{seven}'")
    result = cursor.fetchall()  # Получение всех результатов
    # Получение значений столбца "price"
    pricessale = [row[0] for row in result]
    viruchkasale = 0
    for item in pricessale:
        nums = item.split(',')
        nums = [int(num.strip()) for num in nums]
        viruchkasale += sum(nums)

    # закрываем соединение
    conn.commit()
    conn.close()

    if indexsl == 1:
        captionsl = f"*Ключевая по ученикам*\n\n*Учеников: {count}*\n*Новых учеников: {count24}*\n*Переходов: {count}*\n*Просмотров: {count}*\n*Продаж: {countprice}*"
    elif indexsl == 2:
        captionsl = f"*Финансы*\n\n*Оплат: {countprice}*\n*Выручка: {viruchka}*\n*Сумма скидок: {discount}*\n*Подарено скидок на сумму: {viruchkasale}*"
    elif indexsl == 3:
        captionsl = f"*Переходы*\n\n*Посещений сайта: {count}*\n*Переходов в бота с сайта: {0}*\n*Другие источники: {0}*"
    elif indexsl == 4:
        captionsl = f"*Подписки*\n\n*Активных подписок: {countprice} *\n*Отменено подписок: {0}*"

    markupsl = types.InlineKeyboardMarkup()
    btn_prevsl = types.InlineKeyboardButton(
        "⬅️", callback_data="prev_buttonsl")
    btn_nextsl = types.InlineKeyboardButton(
        "➡️", callback_data="next_buttonsl")
    one = types.InlineKeyboardButton("1 день", callback_data="one1")
    week = types.InlineKeyboardButton("7 дней", callback_data="week2")
    month = types.InlineKeyboardButton("Месяц", callback_data="month3")
    oll = types.InlineKeyboardButton("Все время", callback_data="oll4")
    podr = types.InlineKeyboardButton("Подробнее", callback_data="podr")
    btn_indexsl = types.InlineKeyboardButton(
        f"{indexsl}/{4}", callback_data="current_indexsl"
    )
    markupsl.row(btn_prevsl, btn_indexsl, btn_nextsl)
    markupsl.row(one, week)
    markupsl.row(month, oll)
    markupsl.row(podr)

    if indexst in [1, 2, 3, 4]:
        bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=message.id,
            text=captionsl,
            reply_markup=markupsl,
            parse_mode="Markdown",
        )


def month1(message):
    global captionsl
    global indexsl

    conn = mysql.connector.connect(
        host=host1,
        user=user1,
        password=password1,
        port=port1
    )

    cursor = conn.cursor()
    cursor.execute(namePr)

    # Вычисление даты начала и конца 7-дневного периода
    today = datetime.now().date()
    day30 = today - timedelta(days=1)

    # получить количество учеников
    cursor.execute(
        f"SELECT COUNT(*) FROM пользователи WHERE registration_date >= '{day30}'")
    count = cursor.fetchone()[0]

    # Получение текущей даты и времени
    current_datetime = datetime.now()
    # Вычисление даты и времени, которая была 24 часа назад
    past_datetime = current_datetime - timedelta(hours=24)
    # Преобразование даты и времени в формат, подходящий для SQL-запроса
    past_datetime_str = past_datetime.strftime("%Y-%m-%d %H:%M:%S")
    # Выполнение запроса на подсчет новых учеников
    query = f"SELECT COUNT(*) FROM пользователи WHERE registration_date >= %s AND registration_date >= '{day30}'"
    cursor.execute(query, (past_datetime_str,))
    # Получение результата запроса
    count24 = cursor.fetchone()[0]

    cursor.execute(
        f"SELECT SUM(CEIL(CHAR_LENGTH(price) / 4.5)) FROM пользователи WHERE price != '' AND registration_date >= '{day30}'")
    countprice = cursor.fetchone()[0]

    cursor.execute(
        f"SELECT price FROM пользователи WHERE price != '' AND registration_date >= '{day30}'")
    result = cursor.fetchall()  # Получение всех результатов
    prices = [row[0] for row in result]  # Получение значений столбца "price"
    viruchka = 0
    for item in prices:
        nums = item.split(',')
        nums = [int(num.strip()) for num in nums]
        viruchka += sum(nums)

    cursor.execute(
        f"SELECT COUNT(*) FROM пользователи WHERE discounted_price != '' AND registration_date >= '{day30}'")
    discount = cursor.fetchone()[0]

    cursor.execute(
        f"SELECT price FROM пользователи WHERE discounted_price != '' AND registration_date >= '{day30}'")
    result = cursor.fetchall()  # Получение всех результатов
    # Получение значений столбца "price"
    pricessale = [row[0] for row in result]
    viruchkasale = 0
    for item in pricessale:
        nums = item.split(',')
        nums = [int(num.strip()) for num in nums]
        viruchkasale += sum(nums)

    # закрываем соединение
    conn.commit()
    conn.close()

    if indexsl == 1:
        captionsl = f"*Ключевая по ученикам*\n\n*Учеников: {count}*\n*Новых учеников: {count24}*\n*Переходов: {count}*\n*Просмотров: {count}*\n*Продаж: {countprice}*"
    elif indexsl == 2:
        captionsl = f"*Финансы*\n\n*Оплат: {countprice}*\n*Выручка: {viruchka}*\n*Сумма скидок: {discount}*\n*Подарено скидок на сумму: {viruchkasale}*"
    elif indexsl == 3:
        captionsl = f"*Переходы*\n\n*Посещений сайта: {count}*\n*Переходов в бота с сайта: {0}*\n*Другие источники: {0}*"
    elif indexsl == 4:
        captionsl = f"*Подписки*\n\n*Активных подписок: {countprice} *\n*Отменено подписок: {0}*"

    markupsl = types.InlineKeyboardMarkup()
    btn_prevsl = types.InlineKeyboardButton(
        "⬅️", callback_data="prev_buttonsl")
    btn_nextsl = types.InlineKeyboardButton(
        "➡️", callback_data="next_buttonsl")
    one = types.InlineKeyboardButton("1 день", callback_data="one1")
    week = types.InlineKeyboardButton("7 дней", callback_data="week2")
    month = types.InlineKeyboardButton("Месяц", callback_data="month3")
    oll = types.InlineKeyboardButton("Все время", callback_data="oll4")
    podr = types.InlineKeyboardButton("Подробнее", callback_data="podr")
    btn_indexsl = types.InlineKeyboardButton(
        f"{indexsl}/{4}", callback_data="current_indexsl"
    )
    markupsl.row(btn_prevsl, btn_indexsl, btn_nextsl)
    markupsl.row(one, week)
    markupsl.row(month, oll)
    markupsl.row(podr)

    if indexst in [1, 2, 3, 4]:
        bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=message.id,
            text=captionsl,
            reply_markup=markupsl,
            parse_mode="Markdown",
        )


def oll1(message):
    global captionsl
    global indexsl

    conn = mysql.connector.connect(
        host=host1,
        user=user1,
        password=password1,
        port=port1
    )

    cursor = conn.cursor()
    cursor.execute(namePr)

    # Вычисление даты начала и конца 7-дневного периода
    today = datetime.now().date()
    oll = today - timedelta(days=1)

    # получить количество учеников
    cursor.execute(
        f"SELECT COUNT(*) FROM пользователи WHERE registration_date >= '{oll}'")
    count = cursor.fetchone()[0]

    # Получение текущей даты и времени
    current_datetime = datetime.now()
    # Вычисление даты и времени, которая была 24 часа назад
    past_datetime = current_datetime - timedelta(hours=24)
    # Преобразование даты и времени в формат, подходящий для SQL-запроса
    past_datetime_str = past_datetime.strftime("%Y-%m-%d %H:%M:%S")
    # Выполнение запроса на подсчет новых учеников
    query = f"SELECT COUNT(*) FROM пользователи WHERE registration_date >= %s AND registration_date >= '{oll}'"
    cursor.execute(query, (past_datetime_str,))
    # Получение результата запроса
    count24 = cursor.fetchone()[0]

    cursor.execute(
        f"SELECT SUM(CEIL(CHAR_LENGTH(price) / 4.5)) FROM пользователи WHERE price != '' AND registration_date >= '{oll}'")
    countprice = cursor.fetchone()[0]

    cursor.execute(
        f"SELECT price FROM пользователи WHERE price != '' AND registration_date >= '{oll}'")
    result = cursor.fetchall()  # Получение всех результатов
    prices = [row[0] for row in result]  # Получение значений столбца "price"
    viruchka = 0
    for item in prices:
        nums = item.split(',')
        nums = [int(num.strip()) for num in nums]
        viruchka += sum(nums)

    cursor.execute(
        f"SELECT COUNT(*) FROM пользователи WHERE discounted_price != '' AND registration_date >= '{oll}'")
    discount = cursor.fetchone()[0]

    cursor.execute(
        f"SELECT price FROM пользователи WHERE discounted_price != '' AND registration_date >= '{oll}'")
    result = cursor.fetchall()  # Получение всех результатов
    # Получение значений столбца "price"
    pricessale = [row[0] for row in result]
    viruchkasale = 0
    for item in pricessale:
        nums = item.split(',')
        nums = [int(num.strip()) for num in nums]
        viruchkasale += sum(nums)

    # закрываем соединение
    conn.commit()
    conn.close()

    if indexsl == 1:
        captionsl = f"*Ключевая по ученикам*\n\n*Учеников: {count}*\n*Новых учеников: {count24}*\n*Переходов: {count}*\n*Просмотров: {count}*\n*Продаж: {countprice}*"
    elif indexsl == 2:
        captionsl = f"*Финансы*\n\n*Оплат: {countprice}*\n*Выручка: {viruchka}*\n*Сумма скидок: {discount}*\n*Подарено скидок на сумму: {viruchkasale}*"
    elif indexsl == 3:
        captionsl = f"*Переходы*\n\n*Посещений сайта: {count}*\n*Переходов в бота с сайта: {0}*\n*Другие источники: {0}*"
    elif indexsl == 4:
        captionsl = f"*Подписки*\n\n*Активных подписок: {countprice} *\n*Отменено подписок: {0}*"

    markupsl = types.InlineKeyboardMarkup()
    btn_prevsl = types.InlineKeyboardButton(
        "⬅️", callback_data="prev_buttonsl")
    btn_nextsl = types.InlineKeyboardButton(
        "➡️", callback_data="next_buttonsl")
    one = types.InlineKeyboardButton("1 день", callback_data="one1")
    week = types.InlineKeyboardButton("7 дней", callback_data="week2")
    month = types.InlineKeyboardButton("Месяц", callback_data="month3")
    oll = types.InlineKeyboardButton("Все время", callback_data="oll4")
    podr = types.InlineKeyboardButton("Подробнее", callback_data="podr")
    btn_indexsl = types.InlineKeyboardButton(
        f"{indexsl}/{4}", callback_data="current_indexsl"
    )
    markupsl.row(btn_prevsl, btn_indexsl, btn_nextsl)
    markupsl.row(one, week)
    markupsl.row(month, oll)
    markupsl.row(podr)

    if indexst in [1, 2, 3, 4]:
        bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=message.id,
            text=captionsl,
            reply_markup=markupsl,
            parse_mode="Markdown",
        )


def podr(message):
    statist(message)


indexst = 1
captionst = ""


@bot.message_handler(func=lambda message: message.text == "Статистика")
def statist(message):
    bot.send_message(message.chat.id, "*Статистика*", parse_mode="Markdown")

    global indexst
    global captionst
    indexst = 1
    captionst = "*Просмотров:*\n*Продаж:*\n*Учеников:*\n*Отменено подписок:*\n*Оплата эксперта:*"
    markup = types.InlineKeyboardMarkup()
    btn_prevst = types.InlineKeyboardButton(
        "⬅️", callback_data="prev_buttonst")
    btn_nextst = types.InlineKeyboardButton(
        "➡️", callback_data="next_buttonst")
    one = types.InlineKeyboardButton("1 день", callback_data="one")
    week = types.InlineKeyboardButton("7 дней", callback_data="week")
    month = types.InlineKeyboardButton("Месяц", callback_data="month")
    oll = types.InlineKeyboardButton("Все время", callback_data="oll")
    btn_indexst = types.InlineKeyboardButton(
        f"{indexst}/{6}", callback_data="current_indexst"
    )
    markup.row(btn_prevst, btn_indexst, btn_nextst)
    markup.row(one, week)
    markup.row(month, oll)

    bot.send_message(
        message.chat.id, captionst, reply_markup=markup, parse_mode="Markdown"
    )


def prev_buttonst(message):
    global indexst
    indexst -= 1
    if indexst < 1:
        indexst = 6
    change_textst(message, indexst)


def next_buttonst(message):
    global indexst
    indexst += 1
    if indexst > 6:
        indexst = 1
    change_textst(message, indexst)


def change_textst(message, indexst):
    global captionst

    conn = mysql.connector.connect(
        host=host1,
        user=user1,
        password=password1,
        port=port1
    )

    cursor = conn.cursor()
    cursor.execute(namePr)

    # получить количество учеников
    cursor.execute("SELECT COUNT(*) FROM пользователи")
    count = cursor.fetchone()[0]

    cursor.execute(
        "SELECT SUM(CEIL(CHAR_LENGTH(price) / 4.5)) FROM пользователи WHERE price != ''")
    countprice = cursor.fetchone()[0]

    cursor.execute("SELECT price FROM пользователи WHERE price != ''")
    result = cursor.fetchall()  # Получение всех результатов
    prices = [row[0] for row in result]  # Получение значений столбца "price"
    viruchka = 0
    for item in prices:
        nums = item.split(',')
        nums = [int(num.strip()) for num in nums]
        viruchka += sum(nums)

    # закрываем соединение
    conn.commit()
    conn.close()

    if indexst == 1:
        captionst = f"*Просмотров: {count}*\n*Продаж: {countprice}*\n*Учеников: {count} *\n*Отменено подписок: {0}*\n*Оплата эксперта: как я её должене находить?*"
    elif indexst == 2:
        captionst = f"*Создано программ: {3} *\n*Опубликовано программ: {3} *\n*Учеников: {count}*\n*Оплат: {countprice}*"
    elif indexst == 3:
        captionst = f"*Выручка: {viruchka}*\n*Комиссия эквайринга: мы еще не подключали оплату, я не знаю комиссию банка *"
    elif indexst == 4:
        captionst = f"*Переходов на сайт: {count}*\n*Переходов в бота: {count}*"
    elif indexst == 5:
        captionst = f"*Регистраций: {count}*\n*Зарегистрировано: {count}*\n*Приобретено: чего приобретено? *\n*Не приобретено: чего не приобретено? пиши подробнее*"
    elif indexst == 6:
        captionst = f"*Конверсия в ученика: не знаю что это такое *\n*Конверсия отмены подписки: тоже не знаю*"

    markup = types.InlineKeyboardMarkup()
    btn_prevst = types.InlineKeyboardButton(
        "⬅️", callback_data="prev_buttonst")
    btn_nextst = types.InlineKeyboardButton(
        "➡️", callback_data="next_buttonst")
    one = types.InlineKeyboardButton("1 день", callback_data="one")
    week = types.InlineKeyboardButton("7 дней", callback_data="week")
    month = types.InlineKeyboardButton("Месяц", callback_data="month")
    oll = types.InlineKeyboardButton("Все время", callback_data="oll")
    btn_indexst = types.InlineKeyboardButton(
        f"{indexst}/{6}", callback_data="current_indexst"
    )
    markup.row(btn_prevst, btn_indexst, btn_nextst)
    markup.row(one, week)
    markup.row(month, oll)

    if indexst == 1:
        bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=message.id,
            text=captionst,
            reply_markup=markup,
            parse_mode="Markdown",
        )
    elif indexst == 2:
        bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=message.id,
            text=captionst,
            reply_markup=markup,
            parse_mode="Markdown",
        )
    elif indexst == 3:
        bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=message.id,
            text=captionst,
            reply_markup=markup,
            parse_mode="Markdown",
        )
    elif indexst == 4:
        bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=message.id,
            text=captionst,
            reply_markup=markup,
            parse_mode="Markdown",
        )
    elif indexst == 5:
        bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=message.id,
            text=captionst,
            reply_markup=markup,
            parse_mode="Markdown",
        )
    elif indexst == 6:
        bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=message.id,
            text=captionst,
            reply_markup=markup,
            parse_mode="Markdown",
        )


def one(message):
    global captionst
    global indexst

    conn = mysql.connector.connect(
        host=host1,
        user=user1,
        password=password1,
        port=port1
    )

    cursor = conn.cursor()
    cursor.execute(namePr)

    # Вычисление даты начала и конца 1-дневного периода
    today = datetime.now().date()
    one_day_ago = today - timedelta(days=1)

    # получить количество учеников
    cursor.execute(
        f"SELECT COUNT(*) FROM пользователи WHERE registration_date >= '{one_day_ago}'")
    count = cursor.fetchone()[0]

    cursor.execute(
        f"SELECT SUM(CEIL(CHAR_LENGTH(price) / 4.5)) FROM пользователи WHERE price != '' AND registration_date >= '{one_day_ago}'")
    countprice = cursor.fetchone()[0]

    cursor.execute(
        f"SELECT price FROM пользователи WHERE price != '' AND registration_date >= '{one_day_ago}'")
    result = cursor.fetchall()  # Получение всех результатов
    prices = [row[0] for row in result]  # Получение значений столбца "price"
    viruchka = 0
    for item in prices:
        nums = item.split(',')
        nums = [int(num.strip()) for num in nums]
        viruchka += sum(nums)

    # закрываем соединение
    conn.commit()
    conn.close()

    if indexst == 1:
        captionst = f"*Просмотров: {count}*\n*Продаж: {countprice}*\n*Учеников: {count} *\n*Отменено подписок: {0}*\n*Оплата эксперта: как я её должене находить?*"
    elif indexst == 2:
        captionst = f"*Создано программ: {3} *\n*Опубликовано программ: {3} *\n*Учеников: {count}*\n*Оплат: {countprice}*"
    elif indexst == 3:
        captionst = f"*Выручка: {viruchka}*\n*Комиссия эквайринга: мы еще не подключали оплату, я не знаю комиссию банка *"
    elif indexst == 4:
        captionst = f"*Переходов на сайт: {count}*\n*Переходов в бота: {count}*"
    elif indexst == 5:
        captionst = f"*Регистраций: {count}*\n*Зарегистрировано: {count}*\n*Приобретено: чего приобретено? *\n*Не приобретено: чего не приобретено? пиши подробнее*"
    elif indexst == 6:
        captionst = f"*Конверсия в ученика: не знаю что это такое *\n*Конверсия отмены подписки: тоже не знаю*"

    markup = types.InlineKeyboardMarkup()
    btn_prevst = types.InlineKeyboardButton(
        "⬅️", callback_data="prev_buttonst")
    btn_nextst = types.InlineKeyboardButton(
        "➡️", callback_data="next_buttonst")
    one = types.InlineKeyboardButton("1 день", callback_data="one")
    week = types.InlineKeyboardButton("7 дней", callback_data="week")
    month = types.InlineKeyboardButton("Месяц", callback_data="month")
    oll = types.InlineKeyboardButton("Все время", callback_data="oll")
    btn_indexst = types.InlineKeyboardButton(
        f"{indexst}/{6}", callback_data="current_indexst"
    )
    markup.row(btn_prevst, btn_indexst, btn_nextst)
    markup.row(one, week)
    markup.row(month, oll)

    if indexst in [1, 2, 3, 4, 5, 6]:
        bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=message.id,
            text=captionst,
            reply_markup=markup,
            parse_mode="Markdown",
        )


def week(message):
    global captionst
    global indexst

    conn = mysql.connector.connect(
        host=host1,
        user=user1,
        password=password1,
        port=port1
    )

    cursor = conn.cursor()
    cursor.execute(namePr)

    # Вычисление даты начала и конца 7-дневного периода
    today = datetime.now().date()
    seven = today - timedelta(days=7)

    # получить количество учеников
    cursor.execute(
        f"SELECT COUNT(*) FROM пользователи WHERE registration_date >= '{seven}'")
    count = cursor.fetchone()[0]

    cursor.execute(
        f"SELECT SUM(CEIL(CHAR_LENGTH(price) / 4.5)) FROM пользователи WHERE price != '' AND registration_date >= '{seven}'")
    countprice = cursor.fetchone()[0]

    cursor.execute(
        f"SELECT price FROM пользователи WHERE price != '' AND registration_date >= '{seven}'")
    result = cursor.fetchall()  # Получение всех результатов
    prices = [row[0] for row in result]  # Получение значений столбца "price"
    viruchka = 0
    for item in prices:
        nums = item.split(',')
        nums = [int(num.strip()) for num in nums]
        viruchka += sum(nums)

    # закрываем соединение
    conn.commit()
    conn.close()

    if indexst == 1:
        captionst = f"*Просмотров: {count}*\n*Продаж: {countprice}*\n*Учеников: {count} *\n*Отменено подписок: {0}*\n*Оплата эксперта: как я её должене находить?*"
    elif indexst == 2:
        captionst = f"*Создано программ: {3} *\n*Опубликовано программ: {3} *\n*Учеников: {count}*\n*Оплат: {countprice}*"
    elif indexst == 3:
        captionst = f"*Выручка: {viruchka}*\n*Комиссия эквайринга: мы еще не подключали оплату, я не знаю комиссию банка *"
    elif indexst == 4:
        captionst = f"*Переходов на сайт: {count}*\n*Переходов в бота: {count}*"
    elif indexst == 5:
        captionst = f"*Регистраций: {count}*\n*Зарегистрировано: {count}*\n*Приобретено: чего приобретено? *\n*Не приобретено: чего не приобретено? пиши подробнее*"
    elif indexst == 6:
        captionst = f"*Конверсия в ученика: не знаю что это такое *\n*Конверсия отмены подписки: тоже не знаю*"

    markup = types.InlineKeyboardMarkup()
    btn_prevst = types.InlineKeyboardButton(
        "⬅️", callback_data="prev_buttonst")
    btn_nextst = types.InlineKeyboardButton(
        "➡️", callback_data="next_buttonst")
    one = types.InlineKeyboardButton("1 день", callback_data="one")
    week = types.InlineKeyboardButton("7 дней", callback_data="week")
    month = types.InlineKeyboardButton("Месяц", callback_data="month")
    oll = types.InlineKeyboardButton("Все время", callback_data="oll")
    btn_indexst = types.InlineKeyboardButton(
        f"{indexst}/{6}", callback_data="current_indexst"
    )
    markup.row(btn_prevst, btn_indexst, btn_nextst)
    markup.row(one, week)
    markup.row(month, oll)

    if indexst in [1, 2, 3, 4, 5, 6]:
        bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=message.id,
            text=captionst,
            reply_markup=markup,
            parse_mode="Markdown",
        )


def month(message):
    global captionst
    global indexst

    conn = mysql.connector.connect(
        host=host1,
        user=user1,
        password=password1,
        port=port1
    )

    cursor = conn.cursor()
    cursor.execute(namePr)

    # Вычисление даты начала и конца 7-дневного периода
    today = datetime.now().date()
    day30 = today - timedelta(days=30)

    # получить количество учеников
    cursor.execute(
        f"SELECT COUNT(*) FROM пользователи WHERE registration_date >= '{day30}'")
    count = cursor.fetchone()[0]

    cursor.execute(
        f"SELECT SUM(CEIL(CHAR_LENGTH(price) / 4.5)) FROM пользователи WHERE price != '' AND registration_date >= '{day30}'")
    countprice = cursor.fetchone()[0]

    cursor.execute(
        f"SELECT price FROM пользователи WHERE price != '' AND registration_date >= '{day30}'")
    result = cursor.fetchall()  # Получение всех результатов
    prices = [row[0] for row in result]  # Получение значений столбца "price"
    viruchka = 0
    for item in prices:
        nums = item.split(',')
        nums = [int(num.strip()) for num in nums]
        viruchka += sum(nums)

    # закрываем соединение
    conn.commit()
    conn.close()

    if indexst == 1:
        captionst = f"*Просмотров: {count}*\n*Продаж: {countprice}*\n*Учеников: {count} *\n*Отменено подписок: {0}*\n*Оплата эксперта: как я её должене находить?*"
    elif indexst == 2:
        captionst = f"*Создано программ: {3} *\n*Опубликовано программ: {3} *\n*Учеников: {count}*\n*Оплат: {countprice}*"
    elif indexst == 3:
        captionst = f"*Выручка: {viruchka}*\n*Комиссия эквайринга: мы еще не подключали оплату, я не знаю комиссию банка *"
    elif indexst == 4:
        captionst = f"*Переходов на сайт: {count}*\n*Переходов в бота: {count}*"
    elif indexst == 5:
        captionst = f"*Регистраций: {count}*\n*Зарегистрировано: {count}*\n*Приобретено: чего приобретено? *\n*Не приобретено: чего не приобретено? пиши подробнее*"
    elif indexst == 6:
        captionst = f"*Конверсия в ученика: не знаю что это такое *\n*Конверсия отмены подписки: тоже не знаю*"

    markup = types.InlineKeyboardMarkup()
    btn_prevst = types.InlineKeyboardButton(
        "⬅️", callback_data="prev_buttonst")
    btn_nextst = types.InlineKeyboardButton(
        "➡️", callback_data="next_buttonst")
    one = types.InlineKeyboardButton("1 день", callback_data="one")
    week = types.InlineKeyboardButton("7 дней", callback_data="week")
    month = types.InlineKeyboardButton("Месяц", callback_data="month")
    oll = types.InlineKeyboardButton("Все время", callback_data="oll")
    btn_indexst = types.InlineKeyboardButton(
        f"{indexst}/{6}", callback_data="current_indexst"
    )
    markup.row(btn_prevst, btn_indexst, btn_nextst)
    markup.row(one, week)
    markup.row(month, oll)

    if indexst in [1, 2, 3, 4, 5, 6]:
        bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=message.id,
            text=captionst,
            reply_markup=markup,
            parse_mode="Markdown",
        )


def oll(message):
    global captionst
    global indexst

    conn = mysql.connector.connect(
        host=host1,
        user=user1,
        password=password1,
        port=port1
    )

    cursor = conn.cursor()
    cursor.execute(namePr)

    # Вычисление даты начала и конца 7-дневного периода
    today = datetime.now().date()
    ol = today - timedelta(days=365)

    # получить количество учеников
    cursor.execute(
        f"SELECT COUNT(*) FROM пользователи WHERE registration_date >= '{ol}'")
    count = cursor.fetchone()[0]

    cursor.execute(
        f"SELECT SUM(CEIL(CHAR_LENGTH(price) / 4.5)) FROM пользователи WHERE price != '' AND registration_date >= '{ol}'")
    countprice = cursor.fetchone()[0]

    cursor.execute(
        f"SELECT price FROM пользователи WHERE price != '' AND registration_date >= '{ol}'")
    result = cursor.fetchall()  # Получение всех результатов
    prices = [row[0] for row in result]  # Получение значений столбца "price"
    viruchka = 0
    for item in prices:
        nums = item.split(',')
        nums = [int(num.strip()) for num in nums]
        viruchka += sum(nums)

    # закрываем соединение
    conn.commit()
    conn.close()

    if indexst == 1:
        captionst = f"*Просмотров: {count}*\n*Продаж: {countprice}*\n*Учеников: {count} *\n*Отменено подписок: {0}*\n*Оплата эксперта: как я её должене находить?*"
    elif indexst == 2:
        captionst = f"*Создано программ: {3} *\n*Опубликовано программ: {3} *\n*Учеников: {count}*\n*Оплат: {countprice}*"
    elif indexst == 3:
        captionst = f"*Выручка: {viruchka}*\n*Комиссия эквайринга: мы еще не подключали оплату, я не знаю комиссию банка *"
    elif indexst == 4:
        captionst = f"*Переходов на сайт: {count}*\n*Переходов в бота: {count}*"
    elif indexst == 5:
        captionst = f"*Регистраций: {count}*\n*Зарегистрировано: {count}*\n*Приобретено: чего приобретено? *\n*Не приобретено: чего не приобретено? пиши подробнее*"
    elif indexst == 6:
        captionst = f"*Конверсия в ученика: не знаю что это такое *\n*Конверсия отмены подписки: тоже не знаю*"

    markup = types.InlineKeyboardMarkup()
    btn_prevst = types.InlineKeyboardButton(
        "⬅️", callback_data="prev_buttonst")
    btn_nextst = types.InlineKeyboardButton(
        "➡️", callback_data="next_buttonst")
    one = types.InlineKeyboardButton("1 день", callback_data="one")
    week = types.InlineKeyboardButton("7 дней", callback_data="week")
    month = types.InlineKeyboardButton("Месяц", callback_data="month")
    oll = types.InlineKeyboardButton("Все время", callback_data="oll")
    btn_indexst = types.InlineKeyboardButton(
        f"{indexst}/{6}", callback_data="current_indexst"
    )
    markup.row(btn_prevst, btn_indexst, btn_nextst)
    markup.row(one, week)
    markup.row(month, oll)

    if indexst in [1, 2, 3, 4, 5, 6]:
        bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=message.id,
            text=captionst,
            reply_markup=markup,
            parse_mode="Markdown",
        )
# Запуск бота


bot.polling(none_stop=True)
