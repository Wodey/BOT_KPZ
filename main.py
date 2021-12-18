import json
import logging
from aiogram import Bot, executor, Dispatcher, types
from dotenv import load_dotenv
import os

load_dotenv()

api_token = os.getenv('API_TOKEN')

logging.basicConfig(level=logging.INFO)

bot = Bot(token=api_token)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def send_welcome(message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    keyboard = types.ReplyKeyboardMarkup()
    button_1 = "Хочу"
    keyboard.add(button_1)
    button_2 = "В другой раз..."
    keyboard.add(button_2)
    await message.answer("Хочешь пройти опрос?")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

