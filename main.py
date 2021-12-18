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

question_count = 0

answers = []


@dp.message_handler(commands=['start'])
async def send_welcome(message):
    global question_count
    question_count = 0
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    button_1 = "Хочу"
    keyboard.add(button_1)
    button_2 = "В другой раз..."
    keyboard.add(button_2)
    await message.answer("Хочешь пройти опрос?", reply_markup=keyboard)


@dp.message_handler(lambda message: message.text == "В другой раз...")
async def refuse(message):
    await message.answer("Жаль, но если все таки захочешь, просто напиши /start")


@dp.message_handler(lambda message: message.text == "Хочу")
async def start(message):
    global question_count
    question_count += 1
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    button_1 = "угрозы здоровью"
    button_2 = "угрозы психике детей"
    button_3 = "угрозы конфиденциальности личных данных"
    keyboard.add(button_1)
    keyboard.add(button_2)
    keyboard.add(button_3)
    await message.answer("Какие угрозы или последствия их влияния встречали?", reply_markup=keyboard)


@dp.message_handler(lambda message: question_count == 1)
async def question2(message):
    global question_count
    answers.append(message.text)
    question_count += 1
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    buttons = ["Секты", "Нарко сайты", "Пропаганда расстройств (рпп, психологические расстройства, романтизация "
                                       "курения туда же)", "Неприемлемый контент (порнография, насилие)", "Пропаганда "
                                                                                                          "суицида"]
    for i in buttons:
        keyboard.add(i)
    await message.answer("Какие угрозы психике встречали (из 5 типов)?\n \n 1.Секты \n 2.Нарко сайты \n"
                         " 3.Пропаганда суицида \n "
                         "4.Пропаганда расстройств (рпп, психологические расстройства, романтизация курения туда же)\n"
                         "5.Неприемлемый контент (порнография, насилие)", reply_markup=keyboard)


@dp.message_handler(lambda message: question_count == 2)
async def question_3(message):
    global question_count
    question_count += 1
    answers.append(message.text)
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    buttons = ["pornhub", "xvideos", "vk", "youtube"]
    for i in buttons:
        keyboard.add(i)
    await message.answer("Какие знаете сайты, представляющий угрозу психике детей?", reply_markup=keyboard)


@dp.message_handler(lambda message: question_count == 3)
async def question_4(message):
    global question_count
    question_count += 1
    answers.append(message.text)
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    buttons = ["Sentry", "Google Family Link", "Kidslox", "Kids Tracker", "Screen Time", "Не пользуюсь"]
    for i in buttons:
        keyboard.add(i)
    await message.answer("Какими сервисами для осуществления родительского контроля пользуетесь?",
                         reply_markup=keyboard)


@dp.message_handler(lambda message: question_count == 4)
async def question_5(message):
    global question_count
    question_count += 1
    answers.append(message.text)
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    buttons = ["Да, доверяю", "Нет, не доверяю", "Затрудняюсь ответить"]
    for i in buttons:
        keyboard.add(i)
    await message.answer('Доверяете ли вы Федеральному закону "О защите детей от информации, причиняющей вред их '
                         'здоровью и развитию" ?', reply_markup=keyboard)


@dp.message_handler(lambda message: question_count == 5)
async def question_6(message):
    global question_count
    question_count += 1
    answers.append(message.text)
    qst1 = answers[0]
    qst2 = answers[1]
    qst3 = answers[2]
    qst4 = answers[3]
    qst5 = answers[4]
    questions_str = f'Ваши ответы: \n' \
                    '\n' \
                    'Какие угрозы или последствия их влияния встречали \n' \
                    f'- {qst1} \n' \
                    '\n' \
                    'Какие угрозы психике встречали (из 5 типов)? \n' \
                    f'- {qst2} \n'\
                    '\n' \
                    'Какие знаете сайты, представляющий угрозу психике детей?' \
                    f'- {qst3} \n' \
                    '\n' \
                    'Какими сервисами для осуществления родительского контроля пользуетесь? \n '\
                    f'- {qst4} \n' \
                    '\n' \
                    'Доверяете ли вы Федеральному закону "О защите детей от информации, причиняющей вред их здоровью ' \
                    'и развитию" ?\n' \
                    f'- {qst5} \n' \
                    '\n' \
                    'Спасибо за участие в нашем опросе! Все ваши ответы мы анонимно загрузим в нашу статистику.'
    await message.answer(questions_str, reply_markup=types.ReplyKeyboardRemove())

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
