import config
import telebot
from telebot import types

import pandas as pd
import numpy as np

from datetime import datetime as dt
import pandas_datareader.data as web

import matplotlib.pyplot as plt


bot = telebot.TeleBot(config.TOKEN)

#
# @bot.message_handler(commands=['start'])
# def process_start(message):
#
#     keyboard = telebot.types.ReplyKeyboardMarkup(True)
#     keyboard.row('Меню')
#     msg = bot.send_message(message.chat.id, text = 'Нажми кнопку в меню', reply_markup = keyboard )


@bot.message_handler(content_types = ['text'])
def step1(message):

    menu1 = telebot.types.InlineKeyboardMarkup()
    menu1.add(telebot.types.InlineKeyboardButton(text = 'MA', callback_data ='MA'))
    # menu1.add(telebot.types.InlineKeyboardButton(text = 'EMA', callback_data ='EMA'))


    start = dt(2018,1,1)
    end = dt.today().date()
    print(end)
    try:
        global frame
        frame = web.DataReader(message.text, 'yahoo',start,end)
        stock_data = f'Stock name: {message.text}\nopen:{frame.Open.iloc[-1]}\nhigh: {frame.High.iloc[-1]}\nlow: {frame.Low.iloc[-1]}\nclose:{frame.Close.iloc[-1]}'
    except:
        bot.send_message(message.chat.id,'No stock data')

    msg = bot.send_message(message.chat.id, text ='Выберите тех. индикатор', reply_markup = menu1)

@bot.callback_query_handler(func=lambda call: True)
def step2(call):
    # menu2 = telebot.types.InlineKeyboardMarkup()
    # menu2.add(telebot.types.InlineKeyboardButton(text = 'Третья кнопка', callback_data ='third'))
    # menu2.add(telebot.types.InlineKeyboardButton(text = 'Четвертая кнопка', callback_data ='fourth'))
    global frame
    print(frame)
    print(call.message.chat.id)
    local_frame = frame

    if call.data == 'MA':

        start_price = local_frame.Close.iloc[0]
        print(start_price)

        msg = bot.send_message(call.message.chat.id, 'MA')
        local_frame['MA24'] = local_frame.Close.rolling(24).mean()
        local_frame['Criteria'] = local_frame.Close > local_frame.MA24
        time_in_position = local_frame.Criteria.value_counts()
        local_frame['Returns'] = local_frame.Close.pct_change()
        local_frame['Buy&Hold'] = start_price * (1 + local_frame['Returns']).cumprod()
        local_frame['Strategy'] = start_price * (1 + ( local_frame['Criteria'].shift(1) * local_frame['Returns'] )).cumprod()

        print(local_frame)

        plt.figure(figsize=(9, 3))
        plt.plot(local_frame['Buy&Hold'], label='Купить и держать')
        plt.plot(local_frame['Strategy'], label='Используя стратегию')
        plt.legend()
        plt.savefig('foo.png')

        img = open('foo.png', 'rb')

        bot.send_photo(call.message.chat.id, img)

#
# @bot.message_handler(commands=['start', 'help'])
# def send_welcome(message):
#     bot.send_message(
#         message.chat.id,
#         '''Привет. На данный момент я могу протестировать легкие стратегии, но в скором времени, я научусь давать советы в реальном времени и делать тесты более сложных стратегий.''')
#
#
#
# @bot.callback_query_handler(func=lambda call: True)
# def test_asset_menu(call):
#     print(call)
#     menu1 = telebot.types.InlineKeyboardMarkup()
#     menu1.add(telebot.types.InlineKeyboardButton(text = 'MA', callback_data ='first'))
#     menu1.add(telebot.types.InlineKeyboardButton(text = 'EMA', callback_data ='second'))
#     bot.send_message(message.chat.id, text ='Выберите индикатор', reply_markup = menu1)
#
#
#
# @bot.message_handler(content_types=['text'])
# def response(message):
#     start = dt(2018,1,1)
#     end = dt.today().date()
#     print(end)
#     try:
#         frame = web.DataReader(message.text, 'yahoo',start,end)
#         message_ = f'Stock name: {message.text}\nopen:{frame.Open.iloc[-1]}\nhigh: {frame.High.iloc[-1]}\nlow: {frame.Low.iloc[-1]}\nclose:{frame.Close.iloc[-1]}'
#         msg = bot.send_message(message.chat.id,message_)
#         bot.register_next_step_handler(msg, test_asset_menu, reply_markup=message_)
#     except:
#         bot.send_message(message.chat.id,'No stock data')
#

bot.polling(none_stop=True)
