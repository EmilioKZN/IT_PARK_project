import telebot
import sqlite3
import random
import logging
import datetime

name = 'Emil'


def get_your_best_points(name):
    base = sqlite3.connect('ratingBD.db', check_same_thread=False)
    cur = base.cursor()
    date_str = cur.execute("""SELECT * FROM 'rating' WHERE name = ?;""", (name,)).fetchall()
    max_point = max(date_str)
    return max_point


def your_best_game():
    name1 = name
    max1 = get_your_best_points(name1)
    base = sqlite3.connect('ratingBD.db', check_same_thread=False)
    cur = base.cursor()
    player_str = cur.execute("""SELECT * FROM 'rating'  WHERE name = ?;""", (name1,)).fetchall()
    max2 = min(player_str)
    name2 = max2[0]
    point = max2[1]
    time = max2[2]
    return (f"Твой лучший результат: {name2} \nКоличество очков: {point} \nСправился за: {time}")

print(get_your_best_points(name))

