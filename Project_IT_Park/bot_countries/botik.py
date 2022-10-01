import telebot
import sqlite3
import random
from enum import Enum
token = '5506637372:AAHtzF25c1ZH0xBahElcTjvtECbX--fVFPI'
bot = telebot.TeleBot(token)
count = 0 # Счетчик очков

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

def write_base(answer): # Записываем в БД строку которую выдает бот
    base = sqlite3.connect('dinamicdb.db', check_same_thread=False)
    cur = base.cursor()
    if answers_and_right_str():
        cur.execute("""INSERT INTO 'Dinamicbd'(country, capital, url) VALUES (?, ?, ?);""", answer[0][1:])
        base.commit()

def get_str(): # Выдаем строчку с которой будем сравнивать ответ от пользователя
    base = sqlite3.connect('dinamicdb.db', check_same_thread=False)
    cur = base.cursor()
    return cur.execute("SELECT * FROM 'Dinamicbd'").fetchone()

def clear_base(): # Очищаем БД
    base = sqlite3.connect('dinamicdb.db', check_same_thread=False)
    cur = base.cursor()
    cur.execute("""DELETE FROM 'Dinamicbd'""")
    base.commit()
    cur.close()

# class RightAnswer(Enum):
#     rightanswer = answers_and_right_str()[2]


@bot.message_handler(commands=['start'])
def start_message(message):
    clear_base()
    answers = answers_and_right_str()
    write_base(answers)
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = telebot.types.KeyboardButton(answers[1][0])
    btn2 = telebot.types.KeyboardButton(answers[1][1])
    btn3 = telebot.types.KeyboardButton(answers[1][2])
    btn4 = telebot.types.KeyboardButton(answers[1][3])
    keyboard.add(btn1, btn2, btn3, btn4)
    bot.send_message(message.chat.id, "Привет! " + message.from_user.first_name + " Попроуй угадать страну по флагу")
    bot.send_photo(message.chat.id, photo=answers[0][3], reply_markup=keyboard)


@bot.message_handler(commands=['stop'])
def stop_message(message):
    bot.send_message(message.chat.id, "Игра окончена Ваш счет: " + str(count))


@bot.message_handler(content_types=['text'])
def get_photo(message):
    right_answer = get_str()[0]
    answers = answers_and_right_str()
    if message.text == right_answer:
        clear_base()
        write_base(answers)
        count += 1
        keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = telebot.types.KeyboardButton(answers[1][0])
        btn2 = telebot.types.KeyboardButton(answers[1][1])
        btn3 = telebot.types.KeyboardButton(answers[1][2])
        btn4 = telebot.types.KeyboardButton(answers[1][3])
        keyboard.add(btn1, btn2, btn3, btn4)
        bot.send_message(message.chat.id, "Правильно!" + str(count))
        bot.send_photo(message.chat.id, photo=answers[0][3], reply_markup=keyboard)

    else:
        clear_base()
        write_base(answers)
        keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = telebot.types.KeyboardButton(answers[1][0])
        btn2 = telebot.types.KeyboardButton(answers[1][1])
        btn3 = telebot.types.KeyboardButton(answers[1][2])
        btn4 = telebot.types.KeyboardButton(answers[1][3])
        keyboard.add(btn1, btn2, btn3, btn4)
        bot.send_message(message.chat.id, "Не угадал ( " + str(right_answer))
        bot.send_photo(message.chat.id, photo=answers[0][3], reply_markup=keyboard)



bot.polling(none_stop = True)


