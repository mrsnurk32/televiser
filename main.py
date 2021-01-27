import config
import telebot
import pandas as pd
from datetime import datetime as dt
import pandas_datareader.data as web




bot = telebot.TeleBot(config.TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Hello mate")


@bot.message_handler(content_types=['text'])
def response(message):
    start = dt(2018,1,1)
    end = dt.today().date()
    try:
        frame = web.DataReader(message.text, 'yahoo',start,end)
        message_ = f'Stock name: {message.text}\nopen:{frame.Open.iloc[-1]}\nhigh: {frame.High.iloc[-1]}\nlow: {frame.Low.iloc[-1]}\nclose:{frame.Close.iloc[-1]}'
        bot.send_message(message.chat.id,message_)
    except:
        bot.send_message(message.chat.id,'No stock data')


bot.polling(none_stop=True)
