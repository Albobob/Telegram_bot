import telebot
from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton, ReplyKeyboardMarkup
import bot_dict_sql_request as info
import bot_function as bf

bot = telebot.TeleBot(info.request['token'])


@bot.message_handler(commands=['start', ])
def log_in(message: types.Message):
    user_id = message.from_user.id
    username = message.from_user.username
    bf.insert_user(username, user_id)
    msg_hi = '''Всем привет! Это бот для 'memory' карт.\nНаслаждайтесь освоением своих собственных словарей! '''

    # MENU *** Меню *** meny *** MENU *** Меню *** meny *** MENU
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    # button_1 = types.KeyboardButton('◀  Назад')
    button_2 = types.KeyboardButton('Ваши словари 🗂️')

    # markup.add(button_1, button_2)
    markup.add(button_2)
    bot.send_message(message.chat.id, msg_hi, reply_markup=markup)


@bot.message_handler(content_types=['text'])
def bot_message(message: types.Message):
    user_id = message.from_user.id
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_3 = types.KeyboardButton('Создать словарь 🗂️')
    if message.text == 'Ваши словари 🗂️':
        pack = bf.name_pack(user_id)
        print(len(pack))
        if len(pack) > 0:
            markup.add(button_3)
            bot.send_message(message.chat.id, "Ваши словари:")
            for i in pack:
                bot.send_message(message.chat.id, i)
        else:
            markup.add(button_3)
            bot.send_message(message.chat.id, "У вас нет словарей!", reply_markup=markup)
            if message.text == 'Создать словарь 🗂️':
                bot.send_message(message.chat.id, "Введите название словаря в таком виде:\n*название словаря")
                if message.text[0] == '*':
                    name_pack = message.text.split('*')
                    print(name_pack)
                    # bf.insert_pack(id_profile=user_id, name='')
                    pass
                else:
                    bot.send_message(message.chat.id, "Введите название словаря в таком виде:\n*название словаря")


                pass


#
bot.polling()
