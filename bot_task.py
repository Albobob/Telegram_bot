import telebot
from telebot import types
import info
import json

from pprint import pprint

# from openpyxl import load_workbook
# wb = load_workbook(filename='bd.xlsx')
tb = telebot.TeleBot(info.d_i['token'])

bd = [{
    'user_id': 0,
    'username': '0',
    'first_name': '0'}]

pprint('***')


def bd_rec(user_id, username, first_name):
    crossing = []
    for item in bd:
        bd_user_id = item['user_id']
        bd_username = (item['username'])
        bd_first_name = (item['first_name'])
        print(f'в бд json: {bd_user_id} - в сообщении: {user_id}')

        if user_id == bd_user_id:
            crossing.append(1)

        else:
            crossing.append(0)
    print(crossing)
    print(sum(crossing))

    if sum(crossing) == 0:
        print(f'Новый пользователь!')
        x = {}
        x['user_id'] = user_id
        x['username'] = username
        x['first_name'] = first_name
        bd.append(x)

        file = 'bd_user.json'
        with open(file, 'w', encoding='utf-8') as f:
            json.dump(bd, f, ensure_ascii=False)

    return sum(crossing)


def new_user(new_user_id, first_name):
    x = []
    file = 'bd_user.json'
    with open(file, 'r', encoding='utf-8') as f:
        bd = json.load(f)

        for i in bd:
            if i['user_id'] == new_user_id:
                print(f'Пользователь @{i["username"]} уже в базе')
                x.clear()
                x.append(1)
    if sum(x) > 0:
        return f"{first_name}, ты уже есть в БД не клацай /start"
    else:
        return f'{first_name}, я тебя запишу в БД'


task = {'Написать бота': '645419280',
        'Купить толстовку для Альберта': '198513478',
        'Помочь написать диплом': '198513478'

        }


def task_record(text_task, user_id):
    task[f'{text_task}'] = f'{user_id}'


def task_decode(msg_user_id):
    task_list = []
    task_list.clear()
    for i in task:
        if int(task[i]) == int(msg_user_id):
            task_list.append(i)

    return task_list


@tb.message_handler(commands=['log_in'])
def log_in(message):
    first_name = message.from_user.first_name
    username = message.from_user.username
    user_id = message.from_user.id

    tb.send_message(message.chat.id, new_user(user_id, first_name))
    bd_rec(user_id, username, first_name)


@tb.message_handler(commands=['start'])
def menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item_1 = types.KeyboardButton('/start')
    item_2 = types.KeyboardButton('/log_in')
    item_3 = types.KeyboardButton('/my_task')
    item_4 = types.KeyboardButton('/rec_task')
    markup.add(item_1, item_2, item_3, item_4)

    tb.send_message(message.chat.id, 'Привет', reply_markup=markup)
    log_in(message)


@tb.message_handler(commands=['my_task'])
def my_task(message):
    first_name = message.from_user.first_name
    user_id = message.from_user.id

    task_user = task_decode(user_id)
    tb.send_message(message.chat.id, f'{first_name} твои задачи: ')
    for i in range(len(task_user)):
        tb.send_message(message.chat.id, f'{i + 1}) {task_user[i]}')




    # task_record(message.text, user_id)


tb.polling()
