import telebot
import sqlite3
import random
import logging
import datetime

name = 'Emil'

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

print(get_time(name))

