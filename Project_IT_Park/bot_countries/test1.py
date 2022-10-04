import telebot
import sqlite3
import random
import logging
import datetime

name = 'Владислав'

# def get_time(name):
#     base = sqlite3.connect('staticticDB.db', check_same_thread=False)
#     cur = base.cursor()
#     date_str = cur.execute("""SELECT date FROM 'statistic' WHERE name = ?;""", (name, )).fetchall()[-1][0]
#     date_format = "%Y-%m-%d %H:%M:%S.%f"
#     date_datetime = datetime.datetime.strptime(date_str, date_format)
#     time_now = datetime.datetime.now()
#     deltatime = str(time_now - date_datetime)
#     list_time = deltatime.split(':')
#     hour = list_time[0]
#     minute = list_time[1]
#     sec = list_time[2]
#     return (f"Вы справились за: \nЧасов: {hour}. \nМинут: {minute}. \nСекунд {sec}.")


def get_your_best_points(name):
    base = sqlite3.connect('ratingBD.db', check_same_thread=False)
    cur = base.cursor()
    date_str = cur.execute("""SELECT * FROM 'rating' WHERE name = ?;""", (name,)).fetchall()
    max_point = max(date_str)[1]
    return max_point

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
print(your_best_game())

