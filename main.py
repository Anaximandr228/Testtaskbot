import datetime
import gspread
import telebot
from telebot import types
from yoomoney import Quickpay

API_TOKEN = ''
bot = telebot.TeleBot(API_TOKEN)

table_id = ''
gc = gspread.service_account(filename='testtask-428911-6c0483131d7a.json')

# Выставление счёта и его данных
quickpay = Quickpay(
    receiver="4100118746332228",
    quickpay_form="shop",
    targets="Sponsor this project",
    paymentType="SB",
    sum=2,
)


# Создание Inline-кнопок
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    button_map = types.InlineKeyboardButton("Карты", url='https://yandex.ru/maps/-/CDGS6C0F')
    button_pay = types.InlineKeyboardButton("Оплата", url=quickpay.base_url)
    button_picture = types.InlineKeyboardButton("Изображение", callback_data="pic")
    button_get_value = types.InlineKeyboardButton("Получить значение", callback_data="getvalue")
    button_check_date = types.InlineKeyboardButton("Проверка даты", callback_data="checkdate")
    markup.add(button_map, button_pay, button_picture, button_get_value, button_check_date)
    bot.send_message(message.chat.id,
                     text="Привет, {0.first_name}! Выберите нужную кнопку".format(
                         message.from_user), reply_markup=markup)


# Обработка callback-вызовов
@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.data == 'pic':  # Обработка кнопки отправки изображения
        bot.send_photo(call.message.chat.id, open('img1.png', 'rb'), caption="Текст")

    if call.data == 'getvalue':
        sh = gc.open("гугл_табличка")  # Обработка кнопки для получения значения из Google таблиц
        cell = (sh.sheet1.get('A2'))
        bot.send_message(call.message.chat.id, text=cell)

    if call.data == 'checkdate':
        bot.send_message(call.message.chat.id,
                         text='Введите дату для проверки')  # Обработка кнопки для проверки и записи даты  Google таблицы
        bot.register_next_step_handler(call.message, check_date)
        bot.send_message(call.message.chat.id, text='Дата верна')


# Функция проверки правильности даты
def check_date(message):
    try:
        input_date = message.text
        date_format = '%d.%m.%y'
        datetime.datetime.strptime(input_date, date_format)
    except ValueError:
        bot.send_message(message.chat.id, 'дата неверна')
    return input_date


# Запись данных в Google таблицу
def fill_date(date):
    sh = gc.open("гугл_табличка")
    sh.sheet1.update_cell(2, 2, date)


bot.polling(none_stop=True)
