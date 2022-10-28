import telebot
from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton, ReplyKeyboardMarkup
import bot_dict_sql_request as info
import bot_function as bf

bot = telebot.TeleBot(info.request['token'])

btn = {
    1: 'Меню',
    2: 'Ваши словари',
    3: 'Создать словарь',
    4: 'Создать карточку',
    5: 'Тренироваться',
}


@bot.message_handler(commands=['start', ])
def log_in(message: types.Message):
    user_id = message.from_user.id
    username = message.from_user.username
    bf.insert_user(username, user_id)
    msg_hi = '''Всем привет!\nЭто бот для 'memory' карт.\nНаслаждайтесь освоением своих собственных словарей! '''

    # MENU *** Меню *** meny *** MENU *** Меню *** meny *** MENU
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_menu = types.KeyboardButton(btn[1])
    btn_pack = types.KeyboardButton(btn[2])
    btn_new_pack = types.KeyboardButton(btn[3])
    btn_new_card = types.KeyboardButton(btn[4])
    btn_treining = types.KeyboardButton(btn[5])

    markup.add(btn_pack, btn_new_pack, btn_new_card, btn_treining)

    bot.send_message(message.chat.id, msg_hi, reply_markup=markup)

bot.polling()
