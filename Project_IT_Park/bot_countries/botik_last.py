import telebot
import sqlite3
import random
import datetime
token = '5506637372:AAHtzF25c1ZH0xBahElcTjvtECbX--fVFPI'
bot = telebot.TeleBot(token)
count_answers = 1 # Счетчик флагов
count_right_answers = 0 # Счетчик отчков

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
    if len(answers) != len(set(answers)):
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

@bot.message_handler(commands=['stop'])
def stop_message(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = telebot.types.KeyboardButton('/start')
    keyboard.add(btn1)
    bot.send_message(message.chat.id, "Для начала игры нажмите кнопку '/start'", reply_markup=keyboard)

@bot.message_handler(commands=['yourbestgame'])
def statistic_message(message):
    name = message.from_user.first_name
    def get_your_best_points(name):
        base = sqlite3.connect('ratingBD.db', check_same_thread=False)
        cur = base.cursor()
        date_str = cur.execute("""SELECT * FROM 'rating' WHERE name = ?;""", (name,)).fetchall()
        max_point = max(date_str)
        name2 = max_point[0]
        point = max_point[1]
        time = max_point[2]
        return (f"Твой лучший результат: {name2} \nКоличество очков: {point} \nСправился за: {time}")

    def your_best_game():
        name1 = name
        max1 = get_your_best_points(name1)
        base = sqlite3.connect('ratingBD.db', check_same_thread=False)
        cur = base.cursor()
        player_str = cur.execute("""SELECT * FROM 'rating'  WHERE name = ?;""", (name1, )).fetchall()
        max2 = min(player_str)
        name2 = max2[0]
        point = max2[1]
        time = max2[2]
        return (f"Твой лучший результат: {name2} \nКоличество очков: {point} \nСправился за: {time}")
    bot.send_message(message.chat.id, get_your_best_points(name))

@bot.message_handler(commands=['best'])
def best_message(message):
    def get_max_points():
        base = sqlite3.connect('ratingBD.db', check_same_thread=False)
        cur = base.cursor()
        date_str = cur.execute("""SELECT points FROM 'rating';""").fetchall()
        max_point = max(date_str)[0]
        base.close()
        return max_point

    def best_player():
        max1 = get_max_points()
        base = sqlite3.connect('ratingBD.db', check_same_thread=False)
        cur = base.cursor()
        player_str = cur.execute("""SELECT * FROM 'rating' WHERE points = ?;""", (max1,)).fetchall()
        max2 = min(player_str)
        name = max2[0]
        point = max2[1]
        time = max2[2]
        return (f"Лучший игрок: {name} \nКоличество очков: {point} \nСправился за: {time}")

    bot.send_message(message.chat.id, best_player())

@bot.message_handler(commands=['start'])
def start_message(message):
    date_now = datetime.datetime.now()
    statistic_list = [str(message.from_user.first_name), str(date_now)]
    write_statistic_base(tuple(statistic_list))
    clear_base()
    answers = answers_and_right_str()
    write_base(answers)
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = telebot.types.KeyboardButton(answers[1][0])
    btn2 = telebot.types.KeyboardButton(answers[1][1])
    btn3 = telebot.types.KeyboardButton(answers[1][2])
    btn4 = telebot.types.KeyboardButton(answers[1][3])
    keyboard.add(btn1, btn2, btn3, btn4)
    bot.send_message(message.chat.id, "Привет, " + message.from_user.first_name + "!" + "\n" +
                     "Попробуй угадать страну по флагу." + "\n" + "Вопросов осталось: " + str(11 - count_answers))
    bot.send_photo(message.chat.id, photo=answers[0][3], reply_markup=keyboard)

def write_statistic_base(info):
    base = sqlite3.connect('staticticDB.db', check_same_thread=False)
    cur = base.cursor()
    try:
        cur.execute("""INSERT INTO 'statistic'(name, date) VALUES (?, ?);""", info)
        base.commit()
        base.close()
    except sqlite3.OperationalError:
        base.close()

@bot.message_handler(content_types=['text'])
def get_game(message):
    right_answer = get_str()[0]
    right_answer_capital = get_str()[1]
    answers = answers_and_right_str()
    name = message.from_user.first_name
    global count_answers
    global count_right_answers
    if count_answers <= 10:
        if message.text == right_answer:
            clear_base()
            write_base(answers)
            count_answers += 1
            count_right_answers += 1
            keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = telebot.types.KeyboardButton(answers[1][0])
            btn2 = telebot.types.KeyboardButton(answers[1][1])
            btn3 = telebot.types.KeyboardButton(answers[1][2])
            btn4 = telebot.types.KeyboardButton(answers[1][3])
            keyboard.add(btn1, btn2, btn3, btn4)
            bot.send_message(message.chat.id, "Правильно! Ваш счет: " + str(count_right_answers) + "." + "\n" +
                             "Вопросов осталось - " + str(11 - count_answers))
            bot.send_photo(message.chat.id, photo=answers[0][3], reply_markup=keyboard)
        else:
            count_answers += 1
            clear_base()
            write_base(answers)
            keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = telebot.types.KeyboardButton(answers[1][0])
            btn2 = telebot.types.KeyboardButton(answers[1][1])
            btn3 = telebot.types.KeyboardButton(answers[1][2])
            btn4 = telebot.types.KeyboardButton(answers[1][3])
            keyboard.add(btn1, btn2, btn3, btn4)
            bot.send_message(message.chat.id, "Не угадал (" + "\n" + "Правильный ответ: " + str(right_answer) + "." +
                 "\n" + "Ваш счет: " + str(count_right_answers) + "." + "\n" + "Вопросов осталось - " + str(11 - count_answers))
            bot.send_photo(message.chat.id, photo=answers[0][3], reply_markup=keyboard)
    elif count_answers > 10:
        if message.text == right_answer:
            count_right_answers += 1
            bot.send_message(message.chat.id, "Правильно! Ваш счет: " + str(count_right_answers) + ".")
        else:
            bot.send_message(message.chat.id, "Не угадал (" + "\n" + "Правильный ответ: " + str(right_answer) + ".")
        name = message.from_user.first_name
        liders_list = [str(message.from_user.first_name), int(count_right_answers), str(get_time_datatime_format(name))]
        write_to_rating(tuple(liders_list))
        keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = telebot.types.KeyboardButton('/start')
        keyboard.add(btn1)
        bot.send_message(message.chat.id, "Игра окончена!" + "\n" + "Ваш счет: " + str(count_right_answers) + "." + "\n" +
        str(get_time(name)) + "." + "\n" + "Для начала новой игры нажмите /start.", reply_markup=keyboard)
        count_answers = 0

def get_time(name):
    base = sqlite3.connect('staticticDB.db', check_same_thread=False)
    cur = base.cursor()
    date_str = cur.execute("""SELECT date FROM 'statistic' WHERE name = ?;""", (name, )).fetchall()[-1][0]
    date_format = "%Y-%m-%d %H:%M:%S.%f"
    date_datetime = datetime.datetime.strptime(date_str, date_format)
    time_now = datetime.datetime.now()
    deltatime = str(time_now - date_datetime)
    list_time = deltatime.split(':')
    hour = list_time[0]
    minute = list_time[1]
    sec = list_time[2]
    return (f"Вы справились за: \nЧасов: {hour}. \nМинут: {minute}. \nСекунд {sec}.")

def get_time_datatime_format(name):
    base = sqlite3.connect('staticticDB.db', check_same_thread=False)
    cur = base.cursor()
    date_str = cur.execute("""SELECT date FROM 'statistic' WHERE name = ?;""", (name,)).fetchall()[-1][0]
    date_format = "%Y-%m-%d %H:%M:%S.%f"
    date_datetime = datetime.datetime.strptime(date_str, date_format)
    time_now = datetime.datetime.now()
    deltatime = str(time_now - date_datetime)
    return deltatime

def write_to_rating(info):
    base = sqlite3.connect('ratingBD.db', check_same_thread=False)
    cur = base.cursor()
    cur.execute("""INSERT INTO 'rating'(name, points, time) VALUES (?, ?, ?);""", info)
    base.commit()

bot.polling(none_stop=True)

