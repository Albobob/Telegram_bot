import sqlite3 as sq
import bot_dict_sql_request as dc

name_of_the_database = 'bot_memory.db'
bd = name_of_the_database

user_id = 1


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
            print(f'Запись "{front_side}" уже есть.')
    except:
        print("!!! EROR !!! Слово с ковычками !!! EROR !!! ")



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
        print(f'Пользователь {name} ({id_profile}) уже имеется в {name_of_the_database}')


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


def users_item(id_profile: int) -> []:
    """

    :param id_profile:
    :return: Вывводит все каточки пользователя
    """

    with sq.connect(bd) as con:
        cur = con.cursor()
        #
        cur.execute(f"""
        SELECT * FROM memory_card mc  
        WHERE id_profile == {id_profile}""")
        return [i for i in cur]


def learning_to_write(id_profile: int, memory_card_id: int, ):
    pass


def all_user() -> []:
    return [i[0] for i in sql_request(dc.request['users'])]


print(all_user())
