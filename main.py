import config
import telebot
from telebot import types

import numpy as np

from datetime import datetime as dt
import pandas_datareader.data as web

import matplotlib.pyplot as plt
from televiser import SimpleBackTest


bot = telebot.TeleBot(config.TOKEN)

chats = dict()

@bot.message_handler(content_types = ['text'])
def step1(message):

    menu1 = telebot.types.InlineKeyboardMarkup()
    menu1.add(telebot.types.InlineKeyboardButton(text = 'MA', callback_data ='MA'))

    start = dt(2018,1,1)
    end = dt.today().date()

    try:
        frame = web.DataReader(message.text, 'yahoo',start,end)
        stock_data = f'Stock name: {message.text}\nopen:{frame.Open.iloc[-1]}\nhigh: {frame.High.iloc[-1]}\nlow: {frame.Low.iloc[-1]}\nclose:{frame.Close.iloc[-1]}'

        global chat_list
        chats[message.chat.id] = SimpleBackTest(frame, stock_data)

    except:
        bot.send_message(message.chat.id,'No stock data')

    msg = bot.send_message(message.chat.id, text ='Выберите тех. индикатор', reply_markup = menu1)

@bot.callback_query_handler(func=lambda call: True)
def step2(call):

    data = chats[call.message.chat.id]

    if call.data == 'MA':
        bot.send_photo(call.message.chat.id, data())


bot.polling(none_stop=True)
