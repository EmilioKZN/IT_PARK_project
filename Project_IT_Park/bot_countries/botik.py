import telebot
import sqlite3
import random
from enum import Enum
token = '5506637372:AAHtzF25c1ZH0xBahElcTjvtECbX--fVFPI'
bot = telebot.TeleBot(token)
right_answer = None

class DataBase():

    def __init__(self):
        self.connection = sqlite3.connect('countries.db', check_same_thread=False)
        self.cur = self.connection.cursor()

    def get_all_base(self):
        """Получаем все строки из базы"""
        with self.connection:
            return self.cur.execute("SELECT * FROM 'countries and capitals'").fetchall()

    def one_str(self, rownum):
        """Получаем одну строку по id"""
        with self.connection:
            return self.cur.execute("SELECT * FROM 'countries and capitals' WHERE id = ?", (rownum, )).fetchall()[0]

    def count_rows(self):
        """Считаем количество строк"""
        with self.connection:
            res = self.cur.execute("SELECT * FROM 'countries and capitals'").fetchall()
            return len(res)

    def close_base(self):
        self.connection.close()


def random_capitals(): # Формирование неверных вариантов ответа
    one = DataBase()
    rand_num = random.randint(1, one.count_rows())
    l2 = list()
    for i in range(3):
        rand_num = random.randint(1, one.count_rows())
        l1 = one.one_str(rand_num)
        l2.append(l1[1])
    return l2

def answers_and_right_str(): # Обощение данных
    one = DataBase()
    right_answer_list = one.one_str(random.randint(1, one.count_rows()))
    right_capital = right_answer_list[1]
    answers = [right_capital] + random_capitals()
    random.shuffle(answers)
    try:
        answer = right_answer_list, answers, right_capital
        return answer
    except KeyError:
        return None

# class RightAnswer(Enum):
#     rightanswer = answers_and_right_str()[2]
#
#
#
# print(answers_and_right_str()[0][1:])
# #
@bot.message_handler(commands=['start'])
def start_message(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = telebot.types.KeyboardButton('Старт игры')
    keyboard.add(btn1)
    bot.send_message(message.chat.id, "Привет!" + message.from_user.first_name + "Попроуй угадать страну по флагу", reply_markup=keyboard)
#
@bot.message_handler(content_types=['text'])
def get_photo(message):
    answers = answers_and_right_str()

    if message.text == 'Старт игры':
        keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = telebot.types.KeyboardButton(answers[1][0])
        btn2 = telebot.types.KeyboardButton(answers[1][1])
        btn3 = telebot.types.KeyboardButton(answers[1][2])
        btn4 = telebot.types.KeyboardButton(answers[1][3])
        keyboard.add(btn1, btn2, btn3, btn4)
        bot.send_photo(message.chat.id, photo=answers[0][3], reply_markup=keyboard)

    if message.text == right_answer:
        keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = telebot.types.KeyboardButton(answers[1][0])
        btn2 = telebot.types.KeyboardButton(answers[1][1])
        btn3 = telebot.types.KeyboardButton(answers[1][2])
        btn4 = telebot.types.KeyboardButton(answers[1][3])
        keyboard.add(btn1, btn2, btn3, btn4)
        bot.send_message(message.chat.id, "Правильно!" + str(answers[2]))
        bot.send_photo(message.chat.id, photo=answers[0][3], reply_markup=keyboard)

    else:
        keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = telebot.types.KeyboardButton(answers[1][0])
        btn2 = telebot.types.KeyboardButton(answers[1][1])
        btn3 = telebot.types.KeyboardButton(answers[1][2])
        btn4 = telebot.types.KeyboardButton(answers[1][3])
        keyboard.add(btn1, btn2, btn3, btn4)
        bot.send_message(message.chat.id, "Не угадал (" + str(answers[2]))
        bot.send_photo(message.chat.id, photo=answers[0][3], reply_markup=keyboard)

bot.polling(none_stop = True)


