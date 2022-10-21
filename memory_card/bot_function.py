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


def cards_statistics(id_profile: int, memory_card_id: int) -> dict:
    """
    Отдает статистику по карточке
    :param id_profile: id пользователя
    :param memory_card_id: id карточки
    :return: Отдает статистику по карточке в виде словаря
    """
    data = {
        'wrong': None,
        'correctly': None,
        'count': None,
        'indicator': None,

    }

    with sq.connect(bd) as con:
        cur = con.cursor()
        #
        cur.execute(f"""
        SELECT Sum(wrong) FROM stats_card sc 
        WHERE  id_profile == '{id_profile}' AND memory_card_id == '{memory_card_id}' """)

        for i in cur:
            data['wrong'] = i[0]

        cur.execute(f"""
        SELECT Sum(correctly) FROM stats_card sc 
        WHERE  id_profile == '{id_profile}' AND memory_card_id == '{memory_card_id}' """)

        for i in cur:
            data['correctly'] = i[0]

        cur.execute(f"""
                SELECT count(memory_card_id) FROM stats_card sc 
                WHERE  id_profile == '{id_profile}' AND memory_card_id == '{memory_card_id}' """)

        for i in cur:
            data['count'] = i[0]

    data['indicator'] = data['wrong'] - data['correctly']
    data['percent_of_negative'] = data['indicator'] / data['count']

    return data

    pass


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


def cards_users(id_profile: int) -> list:
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


def cards_learning(id_profile):
    data = []
    """
    Отдает карточики которые тренировал пользователь 
    :param id_profile:
    :return: Вывводит тренируемы каточки пользователя
    """

    with sq.connect(bd) as con:
        cur = con.cursor()
        #
        cur.execute(f"""
        SELECT * FROM stats_card  
        WHERE id_profile == {id_profile}""")
        for i in cur:
            data.append(i)
    return data


def get_memory_card(id_profile: int, memory_card_id: int) -> tuple:
    data = cards_users(id_profile)
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


def all_user() -> list:
    return [i[0] for i in sql_request(dc.request['users'])]


def check_amount_cards(id_profile: int) -> True or False:
    """
    Проверяет есть ли у пользователя карточки
    :param id_profile:
    :return:
    """
    if len(cards_users(id_profile)) > 0:
        return True
    else:
        print('У вас нет ни одной карточки ((')
        return False


def training(id_profile: int):
    first_of_all = []  # Окончательный список с выводом карточек
    card_all = []  # Все карточки пользователя
    card_t = []  # Карточки которые тренеровали
    advice = {}
    if check_amount_cards(id_profile):  # Если у пользователя есть карточки
        for i in cards_users(id_profile):
            card_all.append(i[0])  # Получаю все карточки пользователя

        for i in cards_learning(id_profile):
            card_t.append(i[4])  # Получаю карточки которые тренеровали

        intersect = set(card_all) - set(card_t)  # Получаю карточки которые НЕ тренеровали
        for i in intersect:
            first_of_all.append(i)  # Ставлю на первое место карточки которые НЕ тренеровали

        for i in set(card_t):
            data_advice = cards_statistics(id_profile, i)
            advice[f'{int(i)}'] = data_advice['percent_of_negative']

        for i in ({k: v for k, v in sorted(advice.items(), key=lambda item: item[1])}):  # Сортирую по значению
            first_of_all.append(int(i))

        return first_of_all

        pass
    else:
        print('У пользователя ещё нет карточек')


print(training(645419280))
# print(learning_to_write(645419280, 1))
