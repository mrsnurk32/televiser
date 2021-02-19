import config
import telebot
from telebot import types

import numpy as np

from datetime import datetime as dt
import pandas_datareader.data as web

import matplotlib.pyplot as plt
from televiser import SimpleBackTest

import pandas as pd
import yfinance as fn


bot = telebot.TeleBot(config.TOKEN)

chats = dict()

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, """Привет, я покажу тебе сколько на самом деле приносят тех индикаторы на реальных данных. Введи тикер компании:""")

@bot.message_handler(content_types = ['text'])
def step1(message):
    """
        The function is called when ticker name is sent via message

        The function tries to download stock data, if it fails it sends "no stock data" message
    """

    menu1 = telebot.types.InlineKeyboardMarkup()
    menu1.add(telebot.types.InlineKeyboardButton(text = 'Текущая средняя', callback_data ='moving_average'))
    menu1.add(telebot.types.InlineKeyboardButton(text = 'MACD', callback_data ='macd'))
    menu1.add(telebot.types.InlineKeyboardButton(text = 'EMA', callback_data ='ema'))
    menu1.add(telebot.types.InlineKeyboardButton(text = 'Stockhastic', callback_data ='stockhastic'))    
   
    start = dt(2018,1,1)
    end = dt.today().date()

    try:
        # frame = web.DataReader(message.text, 'yahoo',start,end)
        frame = fn.download(message.text, start, end)
        frame = pd.DataFrame(frame)

    except Exception as err:
        print(err)
        bot.send_message(message.chat.id,'No stock data')

    else:
        stock_data = f'Stock name: {message.text.upper()}\nopen:{frame.Open.iloc[-1]}\nhigh: {frame.High.iloc[-1]}\nlow: {frame.Low.iloc[-1]}\nclose:{frame.Close.iloc[-1]}'
        global chat_list
        chats[message.chat.id] = SimpleBackTest(frame, stock_data, message.text)
        msg = bot.send_message(message.chat.id, text ='Выберите тех. индикатор', reply_markup = menu1)


@bot.callback_query_handler(func=lambda call: True)
def step2(call):
    """
        The function is called when indicator is chosen

        Then it runs backtest and returns performance image
    """

    data = chats[call.message.chat.id]
    bot.send_photo(call.message.chat.id, data(indicator=call.data))
    bot.send_message(call.message.chat.id,text = data.ev_message)


bot.polling(none_stop=True)
