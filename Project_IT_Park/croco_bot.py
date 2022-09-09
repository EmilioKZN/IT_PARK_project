from get_words import *
import telebot
token = '5506637372:AAHtzF25c1ZH0xBahElcTjvtECbX--fVFPI'
bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start'])
def start_message(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = telebot.types.KeyboardButton('Легкий')
    btn2 = telebot.types.KeyboardButton('Средний')
    btn3 = telebot.types.KeyboardButton('Сложный')
    keyboard.add(btn1, btn2, btn3)
    bot.send_message(message.chat.id, get_hello_txt(), reply_markup=keyboard)

@bot.message_handler(content_types=['text'])
def send_word(message):
    if(message.text == "Легкий"):
        keyboard = telebot.types.ReplyKeyboardMarkup()
        btn1 = telebot.types.KeyboardButton("Угадал")
        btn2 = telebot.types.KeyboardButton("Неугадал")
        keyboard.add(btn1, btn2)
        bot.send_message(message.chat.id, get_ez(), reply_markup=keyboard)
    if (message.text == "Угадал"):
            bot.send_message(message.chat.id, get_ez())
    if (message.text == "Неугадал"):
            bot.send_message(message.chat.id, get_ez())
#
#
# @bot.message_handler(content_types=['text'])
# def send_word1(message):
    if(message.text == "Средний"):
        keyboard = telebot.types.ReplyKeyboardMarkup()
        btn1 = telebot.types.KeyboardButton("Угадaл")
        btn2 = telebot.types.KeyboardButton("Неугадaл")
        keyboard.add(btn1, btn2)
        bot.send_message(message.chat.id, get_norm(), reply_markup=keyboard)
    elif (message.text == "Угадaл"):
        bot.send_message(message.chat.id, get_norm())
    elif (message.text == "Неугадaл"):
        bot.send_message(message.chat.id, get_norm())

# @bot.message_handler(content_types=['text'])
# def send_word2(message):
    if(message.text == "Сложный"):
        keyboard = telebot.types.ReplyKeyboardMarkup()
        btn1 = telebot.types.KeyboardButton("Угaдал")
        btn2 = telebot.types.KeyboardButton("Неyгадал")
        keyboard.add(btn1, btn2)
        bot.send_message(message.chat.id, get_diff(), reply_markup=keyboard)
    elif (message.text == "Угaдал"):
        bot.send_message(message.chat.id, get_diff())
    elif (message.text == "Неyгадал"):
        bot.send_message(message.chat.id, get_diff())

bot.polling(none_stop = True)
