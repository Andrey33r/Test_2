import telebot
from config import *
from currency_converter import CurrencyConverter
from telebot import types

bot = telebot.TeleBot(TOKEN)
currency = CurrencyConverter()
amount = 0


@bot.message_handler(commands=['start'])
def start(message):
    mess = f"Привет {message.from_user.first_name}!\n" \
           f"\n" \
           f"Я Бот, который поможет Вам конвертировать валюты.\n" \
           f"Введите количество купюр.\n" \
           f"\n" \
           f"Если Вам потребуется помощь, нажмите /help"

    bot.send_message(message.chat.id, mess)


@bot.message_handler(commands=['help'])
def knopka(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    helper = types.KeyboardButton('HELP')
    markup.add(helper)
    bot.send_message(message.chat.id, f'{message.from_user.first_name} вот кнопка HELP', reply_markup=markup)


@bot.message_handler()
def summa(message):
    if message.text == 'HELP':
        mess = f"{message.from_user.first_name}, введите количество купюр и выбирите передложенную пару валют.\n" \
               f" ВАЖНО!!!\n Дробное число водить через знак точка."
        bot.send_message(message.chat.id, mess)
    else:
        global amount
        try:
            amount = float(message.text.strip())
        except Exception:
            bot.send_message(message.chat.id, 'Некоректный формат, введите сумму')
            return

        if amount > 0:
            markup = types.InlineKeyboardMarkup(row_width=2)
            btn1 = types.InlineKeyboardButton('USD/EUR', callback_data='usd/eur')
            btn2 = types.InlineKeyboardButton('EUR/USD', callback_data='eur/usd')
            btn3 = types.InlineKeyboardButton('USD/RUB', callback_data='usd/rub')
            btn4 = types.InlineKeyboardButton('RUB/USD', callback_data='rub/usd')
            btn5 = types.InlineKeyboardButton('EUR/RUB', callback_data='eur/rub')
            btn6 = types.InlineKeyboardButton('RUB/EUR', callback_data='rub/eur')
            markup.add(btn1, btn2, btn3, btn4, btn5, btn6)
            bot.send_message(message.chat.id, 'Выберите пару валют', reply_markup=markup)
        else:
            bot.send_message(message.chat.id, 'Введите число больше нуля')


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    values = call.data.upper().split('/')
    res = currency.convert(amount, values[0], values[1])
    bot.send_message(call.message.chat.id, f'После конвертации: {round(res, 2)}. \nМожете ввести сумму еще раз.')


bot.polling(none_stop=True)
