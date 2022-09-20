import telebot
import sqlite3
import random
token = '5506637372:AAHtzF25c1ZH0xBahElcTjvtECbX--fVFPI'
bot = telebot.TeleBot(token)
base_for_bot = sqlite3.connect('countries.db')
cur = base_for_bot.cursor()

class data_base():

    def get_randon_str(self):
        """Выдаем рандомную строчку из таблицы с правильным ответом и флагом"""
        cur.execute("SELECT * FROM 'countries and capitals' ORDER BY RANDOM() LIMIT 1;")
        one_result = cur.fetchone()
        return one_result

    def get_countries_value(self):
        """Формируем варинты ответов"""
        random_list = [self.get_randon_str()[1]]
        for i in range(3):
            random_list.append(self.get_randon_str()[1])
        return random_list

    def get_flag(self):
        """Выдаем ссылку на изображение флага"""
        country_flag = self.get_randon_str()[3]
        return str(country_flag)



bas = data_base().get_flag()
#print(bas.get_countries_value())
#print(bas.get_randon_str())
#print(bas.get_flag())


@bot.message_handler(commands=['start'])
def start_message(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = telebot.types.KeyboardButton('Старт игры')
    keyboard.add(btn1)
    bot.send_message(message.chat.id, "Попроуй угадать страну по флагу", reply_markup=keyboard)
    bot.send_photo(message.chat.id, photo=bas, reply_markup=keyboard)

bot.polling(none_stop = True)
# @bot.message_handler(content_types=['photo'])
# def send_flag(message):
#     if(message.text == 'Старт игры'):
#         base = data_base()
#         # keyboard = telebot.types.ReplyKeyboardMarkup()
#         # btn1 = telebot.types.KeyboardButton(base.get_countries_value()[0])
#         # btn2 = telebot.types.KeyboardButton(base.get_countries_value()[1])
#         # btn3 = telebot.types.KeyboardButton(base.get_countries_value()[2])
#         # btn4 = telebot.types.KeyboardButton(base.get_countries_value()[3])
#         # keyboard.add(btn1, btn2, btn3, btn4)
#         photo = base.get_flag()
#         bot.send_photo(message.chat.id, photo=base.get_flag(), reply_markup=keyboard)


