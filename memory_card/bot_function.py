import sqlite3 as sq
import bot_dict_sql_request as dc

name_of_the_database = 'bot_memory.db'
bd = name_of_the_database

user_id = 1


# Работа с Базой данных
def sql_request(request: str) -> []:
    data = []
    with sq.connect(bd) as con:
        cur = con.cursor()
        cur.execute(request)
        for i in cur:
            data.append(i)

    return data


def insert_memory_card(front_side: str, reverse_side: str, id_profile: int) -> None:
    """
    :param front_side: Внешняя сторона карточки
    :param reverse_side: Обратная сторона карточки
    :param id_profile: Пользователь (id)
    :return:
    """
    try:
        reverse_side = reverse_side.lower().capitalize()
        front_side = front_side.lower().capitalize()

        if check_uniq_column('memory_card', 'front_side', front_side):
            with sq.connect(bd) as con:
                cur = con.cursor()
                #
                cur.execute(f"""
            INSERT INTO memory_card (front_side, reverse_side, id_profile)
            VALUES('{front_side}', '{reverse_side}', {id_profile})
                    """)
        else:
            pass
            # print(f'Запись "{front_side}" уже есть.')
    except:
        print("!!! EROR !!! Слово с ковычками !!! EROR !!! ")


def insert_stats_card(id_profile: int, memory_card_id: int, response: True or False) -> None:
    """

    :param id_profile: id Пользователя
    :param memory_card_id: id Карточки
    :param response: Ответ пользователя (True или False)
    :return: Если пользоваель ответил правильно...
    """
    if response:
        with sq.connect(bd) as con:
            cur = con.cursor()
            cur.execute(f"""
        INSERT INTO stats_card (memory_card_id, id_profile, correctly )
        VALUES('{memory_card_id}', {id_profile}, {1})
                """)
    else:
        with sq.connect(bd) as con:
            cur = con.cursor()
            cur.execute(f"""
        INSERT INTO stats_card (memory_card_id, id_profile, wrong )
        VALUES('{memory_card_id}', {id_profile}, {1})
                """)

    pass


def insert_user(name: str, id_profile: int) -> None:
    """
    Проверяет имеется ли пользователь в БД и записывает если он отстутствует
    :param id_profile: id пользователя
    :param name: имя пользователя
    :return: Записывает в таблицу 'users' пользователя
    """
    if check_uniq_column('users', 'id_profile', id_profile):
        with sq.connect(bd) as con:
            cur = con.cursor()
            cur.execute(f"""
        INSERT INTO users (name, id_profile)
        VALUES('{name}', {id_profile})
                """)
    else:
        pass
        # print(f'Пользователь {name} ({id_profile}) уже имеется в {name_of_the_database}')


# Работа с данными из БД
def check_uniq_column(name_table: str, name_column: str, check_value) -> True or False:
    """
    Проверяет уникальность добавляемого значения
    :rtype: object
    :param name_table: Название таблицы
    :param name_column: Название колонки
    :param check_value: Искомое значение
    :return: False - совпадение найдено | True - совпадение не найдено (check_value нет)
    """
    check = []
    with sq.connect(bd) as con:
        cur = con.cursor()
        #
        cur.execute(f"""
        SELECT {name_column} FROM {name_table} 
        WHERE {name_column} == "{check_value}"
                """)

        for i in cur:
            check.append(i)

        if len(check) > 0:
            return False
        else:
            return True


def users_item(id_profile: int):
    data = []
    """
    Отдает карточик пользователя
    :param id_profile:
    :return: Вывводит все каточки пользователя
    """

    with sq.connect(bd) as con:
        cur = con.cursor()
        #
        cur.execute(f"""
        SELECT * FROM memory_card mc  
        WHERE id_profile == {id_profile}""")
        for i in cur:
            data.append(i)
    return data


def get_memory_card(id_profile: int, memory_card_id: int) -> tuple:
    data = users_item(id_profile)
    for i in data:
        if memory_card_id == int(i[0]):
            reverse_side = i[3]
            front_side = i[2]
            return front_side, reverse_side

    pass


def learning_to_write(id_profile: int, memory_card_id: int):
    card = get_memory_card(id_profile, memory_card_id)
    response_user = input(f'Обратная сторона карточки: |{card[1]}|\nВведите лицевую сторону карточки >>> ').lower()
    if response_user == card[0].lower():
        insert_stats_card(id_profile, memory_card_id, True)
    else:
        insert_stats_card(id_profile, memory_card_id, False)
    pass


def all_user() -> []:
    return [i[0] for i in sql_request(dc.request['users'])]


def check_amount_cards(id_profile: int) -> True or False:
    """
    Проверяет есть ли у пользователя карточки
    :param id_profile:
    :return:
    """
    if len(users_item(id_profile)) > 0:
        return True
    else:
        print('У вас нет ни одной карточки ((')
        return False


def training(id_profile: int):
    card_all = []
    card_t = []
    if check_amount_cards(id_profile):
        for i in users_item(id_profile):
            card_all.append(i[0])
        print(card_all)
        pass
    else:
        pass


print(training(645419280))
