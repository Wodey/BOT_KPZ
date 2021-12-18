import json
import logging
from aiogram import Bot, executor, Dispatcher, types
from dotenv import load_dotenv
import os
from db import Database

load_dotenv()

api_token = os.getenv('API_TOKEN')

logging.basicConfig(level=logging.INFO)

bot = Bot(token=api_token)
dp = Dispatcher(bot)

question_count = 0

answers = []
global_answers = []
# База данных
my_db = Database()


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
    my_db.upload_question(1, message.text)
    question_count += 1
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    buttons = ["Секты", "Нарко сайты", "Пропаганда расстройств (рпп, психологические расстройства, романтизация "
                                       "курения туда же)", "Неприемлемый контент (порнография, насилие)", "Пропаганда "
                                                                                                          "суицида"]
    for i in buttons:
        keyboard.add(i)
    await message.answer("Какие угрозы психике встречали (из 5 типов)?", reply_markup=keyboard)


@dp.message_handler(lambda message: question_count == 2)
async def question_3(message):
    global question_count
    question_count += 1
    answers.append(message.text)
    my_db.upload_question(2, message.text)
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
    my_db.upload_question(3, message.text)
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
    my_db.upload_question(4, message.text)
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
    my_db.upload_question(5, message.text)
    qst1 = answers[0]
    global_answers.append(my_db.get_question_count(1))
    your_stat_1 = global_answers[0].pop(qst1)
    qst2 = answers[1]
    global_answers.append(my_db.get_question_count(2))
    your_stat_2 = global_answers[1].pop(qst2)
    qst3 = answers[2]
    global_answers.append(my_db.get_question_count(3))
    your_stat_3 = global_answers[2].pop(qst3)
    qst4 = answers[3]
    global_answers.append(my_db.get_question_count(4))
    your_stat_4 = global_answers[3].pop(qst4)
    qst5 = answers[4]
    global_answers.append(my_db.get_question_count(5))
    your_stat_5 = global_answers[4].pop(qst5)

    global_answers_1 = f'Ваша позиция - {your_stat_1} \n'
    for i in list(global_answers[0].keys()):
        global_answers_1 += f'{i} - {global_answers[0][i]} \n'

    global_answers_2 = f'Ваша позиция - {your_stat_2} \n'
    for i in list(global_answers[1].keys()):
        global_answers_2 += f'{i} - {global_answers[1][i]} \n'

    global_answers_3 = f'Ваша позиция - {your_stat_3} \n'
    for i in list(global_answers[2].keys()):
        global_answers_3 += f'{i} - {global_answers[2][i]} \n'

    global_answers_4 = f'Ваша позиция - {your_stat_4} \n'
    for i in list(global_answers[3].keys()):
        global_answers_4 += f'{i} - {global_answers[3][i]} \n'

    global_answers_5 = f'Ваша позиция - {your_stat_5} \n'
    for i in list(global_answers[4].keys()):
        global_answers_5 += f'{i} - {global_answers[4][i]} \n'


    questions_str = f'Ваши ответы: \n' \
                    '\n' \
                    '1. Какие угрозы или последствия их влияния встречали \n' \
                    f'- {qst1} \n' \
                    '\n' \
                    'Ответы других участников: \n' + global_answers_1 + '\n' \
                    '\n' \
                    '2. Какие угрозы психике встречали (из 5 типов)? \n' \
                    f'- {qst2} \n' \
                    '\n' \
                    'Ответы других участников: \n' + global_answers_2 + '\n' \
                    '\n' \
                    '3. Какие знаете сайты, представляющий угрозу психике детей? \n' \
                    f'- {qst3} \n' \
                    '\n' \
                    'Ответы других участников: \n' + global_answers_3 + '\n' \
                    '\n' \
                    '4. Какими сервисами для осуществления родительского контроля пользуетесь? \n' \
                    f'- {qst4} \n' \
                    '\n' \
                    'Ответы других участников: \n' + global_answers_4 + '\n' \
                    '\n' \
                    '5. Доверяете ли вы Федеральному закону "О защите детей от информации, причиняющей вред их здоровью ' \
                    'и развитию" ?\n' \
                    f'- {qst5} \n' \
                    '\n' \
                    'Ответы других участников: \n' + global_answers_5 + '\n ' \
                    '\n' \
                    'Спасибо за участие в нашем опросе! Все ваши ответы мы анонимно загрузим в нашу статистику.'
    await message.answer(questions_str, reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(commands=['test'])
async def test(message):
    response = my_db.get_question_count("1")
    print(response)
    await message.answer("ok")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
