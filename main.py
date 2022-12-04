import logging
from telegram import Update
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler, ContextTypes
from telegram.ext import CommandHandler
from telegram.ext import ContextTypes

import requests
APPID = "19c8ce8cb576ac1afc61f2f3d6c5b140"  # <-- Put your OpenWeatherMap appid here!
URL_BASE = "https://api.openweathermap.org/data/2.5/"


def current_weather(q: str = "Kiev", appid: str = APPID) -> dict:
    """https://openweathermap.org/api"""
    return requests.get(URL_BASE + "weather", params=locals()).json()


def weather_forecast(q: str = "Kolkata, India", appid: str = APPID) -> dict:
    """https://openweathermap.org/forecast5"""
    return requests.get(URL_BASE + "forecast", params=locals()).json()


def weather_onecall(lat: float = 55.68, lon: float = 12.57, appid: str = APPID) -> dict:
    """https://openweathermap.org/api/one-call-api"""
    return requests.get(URL_BASE + "onecall", params=locals()).json()









logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="I'm a bot, who is going to show you the API info right from the internet![doggy]!"
    )

async def weather(update: Update, context: ContextTypes.DEFAULT_TYPE):
    from pprint import pprint
    #location = input("Enter a location:").strip()
    location = ' '.join(context.args)
    if location:
        pprint(current_weather(location))
        temperature = (current_weather(location)['main']['temp'] - 273.15)
    await context.bot.send_message(

        chat_id = update.effective_chat.id,
        text = "It's " + str(round(temperature,3)) + '° in ' + location
    )

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='Yeah your sating smth rrrrrrrreeeeeeeeeealy smart!!'
    )

async def caps(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text_caps = ' '.join(context.args).upper()
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=text_caps
    )
async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")






















if __name__ == '__main__':

    application = ApplicationBuilder().token('5864168300:AAGLtYZLQxz2Sqt2xdFkNL1LSKPmsJFoH98').build()

    weather_handler = CommandHandler('weather', weather)
    caps_handler = CommandHandler('caps', caps)
    unknown_handler = MessageHandler(filters.COMMAND, unknown)
    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
    start_handler = CommandHandler('start', start)

    application.add_handler(weather_handler)
    application.add_handler(start_handler)
    application.add_handler(caps_handler)
    application.add_handler(echo_handler)
    application.add_handler(unknown_handler)


    application.run_polling()