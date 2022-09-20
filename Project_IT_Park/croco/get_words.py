import random
import time
f = open("words_crocodile.txt", "r", encoding='UTF-8')

words = f.readlines()

words_ease = list(words[0].split("'"))

for i in words_ease:
    if i == "]\n":
       words_ease.remove(i)
    elif i == "[":
        words_ease.remove(i)
    elif i == ", ":
        words_ease.remove(i)

def get_ez():
    num = random.randint(0, len(words_ease) - 1)
    return words_ease[num]

words_normal = list(words[1].split("'"))

for i in words_normal:
    if i == "]\n":
       words_normal.remove(i)
    elif i == "[":
        words_normal.remove(i)
    elif i == ", ":
        words_normal.remove(i)

def get_norm():
    num = random.randint(0, len(words_normal) - 1)
    return words_normal[num]

words_difficult = list(words[2].split("'"))

for i in words_difficult:
    if i == "]\n":
       words_difficult.remove(i)
    elif i == "[":
        words_difficult.remove(i)
    elif i == ", ":
        words_difficult.remove(i)

def get_diff():
    num = random.randint(0, len(words_normal) - 1)
    return words_difficult[num]

def get_hello_txt():
    return "Добро пожаловать в игру 'Крокодил', выберите уровень сложности"

def get_stop():
    time.sleep(5)
    return "Стоп"




#print(get_ez(), get_norm(), get_diff())