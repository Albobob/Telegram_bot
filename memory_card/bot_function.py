import sqlite3 as sq
import bot_dict_sql_request as dc

name_of_the_database = 'bot_memory.db'
bd = name_of_the_database

user_id = 1


# Работа с Базой данных
def sql_request(request: str) -> list:
    """

    :param request: Запрос в базу данных
    :return:
    """
    data = []
    with sq.connect(bd) as con:
        cur = con.cursor()
        cur.execute(request)
        for i in cur:
            data.append(i)

    return data


def insert_memory_card(front_side: str, reverse_side: str, id_profile: int) -> None:
    # front_side: str, reverse_side: str,
    """
    Добавление в БД карточки
    :param front_side: Внешняя сторона карточки
    :param reverse_side: Обратная сторона карточки
    :param id_profile: Пользователь (id)
    :return:
    """
    front_side = front_side.lower().capitalize()
    reverse_side = reverse_side.lower().capitalize()
    try:
        print(front_side)
        print(reverse_side)

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
    Добавление данных в БД таблица  stats_card
    :param id_profile: Пользователь (id)
    :param memory_card_id: id Карточки
    :param response: Ответ пользователя (True или False)
    :return: Если пользоваель ответил правильно
     записывается 1 в слобец correctly,
     елси непраильно в стобец wrong
    """
    if response:
        with sq.connect(bd) as con:
            cur = con.cursor()
            cur.execute(f"""
        INSERT INTO stats_card (memory_card_id, id_profile, correctly, wrong )
        VALUES('{memory_card_id}', {id_profile}, {1}, {0})
                """)
    else:
        with sq.connect(bd) as con:
            cur = con.cursor()
            cur.execute(f"""
        INSERT INTO stats_card (memory_card_id, id_profile, correctly, wrong )
        VALUES('{memory_card_id}', {id_profile}, {0},{1})
                """)

    pass


def insert_user(name: str, id_profile: int) -> None:
    """
    Проверяет Записывает пользователя в БД если он отсутствует
    :param id_profile: Пользователь (id)
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
        print(f'Пользователь {name} ({id_profile}) уже имеется в {name_of_the_database}')


def cards_statistics(id_profile: int, memory_card_id: int) -> dict:
    """
    Отдает статистику по карточке
    :param id_profile: Пользователь (id)
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

    if data['wrong'] or data['correctly'] is not None:
        data['indicator'] = data['wrong'] - data['correctly']
        data['percent_of_negative'] = data['indicator'] / data['count']
    else:
        print('Карточки не тренировались')

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
    """
    Отдает карточик пользователя
    :param id_profile: Пользователь (id)
    :return: Вывводит все каточки пользователя
    """
    data = []
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
    """
    Отдает карточики которые тренировал пользователь 
    :param id_profile: Пользователь (id)
    :return: Вывводит тренируемы каточки пользователя
    """
    data = []
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
    """
    Отдает искомую карточку
    :param id_profile: Пользователь (id)
    :param memory_card_id: id Карточки
    :return:
    """
    data = cards_users(id_profile)
    for i in data:
        if memory_card_id == int(i[0]):
            reverse_side = i[3]
            front_side = i[2]
            return front_side, reverse_side

    pass


def learning_to_write(id_profile: int, memory_card_id: int):
    """

    :param id_profile:
    :param memory_card_id:
    :return:
    """
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
    :param id_profile: Пользователь (id)
    :return:
    """
    if len(cards_users(id_profile)) > 0:
        return True
    else:
        print('У вас нет ни одной карточки ((')
        return False


def training_list(id_profile: int):
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

        for i in (
                {k: v for k, v in
                 sorted(advice.items(), key=lambda item: item[1], reverse=True)}):  # Сортирую по значению
            first_of_all.append(int(i))

        return first_of_all

        pass
    else:
        print('У пользователя ещё нет карточек')


def start_training(id_profile: int):
    recommended_cards = training_list(id_profile)
    for i in recommended_cards:
        learning_to_write(id_profile, i)


def name_pack(id_profile: int) -> list:
    """
    Возвращает словари пользователя
    :param id_profile:
    :return:
    """
    with sq.connect(bd) as con:
        data = []
        cur = con.cursor()
        #
        cur.execute(f"""
        SELECT name  FROM pack 
        WHERE id_profile == '{id_profile}'
                """)
        for i in cur:
            data.append(i)
        return data

    pass


def insert_pack(id_profile: int, name: str) -> None:
    with sq.connect(bd) as con:
        cur = con.cursor()
        #
        cur.execute(f"""
    INSERT INTO pack (id_profile, name)
    VALUES('{id_profile}', '{name}')
            """)
