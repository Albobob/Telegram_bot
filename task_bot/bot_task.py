import telebot
from telebot import types
import info
import json
import task_sheet
from pprint import pprint

bot = telebot.TeleBot(info.d_i['token'])

bd = {645419280: 'Симонян А.Р.',
      202383142: 'Криушин Д.С.',
      222361465: 'Королев А.А.',
      898701620: 'Миронова А.А.', }


# MENU *** Меню *** meny *** Меню *** meny
@bot.message_handler(commands=['start'])
def log_in(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_task = 'my_task'
    markup.add(button_task)
    bot.send_message(message.chat.id, f'Привет {message.from_user.first_name} твои задачи:', reply_markup=markup)


# MENU *** Меню *** meny *** Меню *** meny

@bot.message_handler(content_types=['text'])
# Проверка наличие ID в БД
def bot_message(message):
    for i in bd:
        crossing = []
        crossing.clear()
        if str(message.from_user.id) == str(i):
            crossing.append(1)
        if sum(crossing) != 0:
            print(f'Я нашел пользователя в БД как {bd[i]}')
            break
        else:
            print('Пользователя нет в БД')
            bot.send_message(message.chat.id, 'Пользователя нет в БД напиши @albobob')
            break


# Получаем список заданй
# def task(message):
#     task_sheet.push_task(message.from_user.id)


bot.polling()
