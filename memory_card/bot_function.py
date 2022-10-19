import sqlite3 as sq
import bot_dict_sql_request as dc

name_of_the_database = 'bot_memory.db'
bd = name_of_the_database

front_side = 'answer'
front_side = front_side.lower().capitalize()
reverse_side = 'ответ'
reverse_side = reverse_side.lower().capitalize()
user_id = 1


def sql_request(request: str) -> []:
    data = []
    with sq.connect(bd) as con:
        cur = con.cursor()
        cur.execute(request)
        for i in cur:
            data.append(i)

    return data


def insert_memory_card(front_side: str, reverse_side: str, user_id: int) -> None:
    """
    :param front_side: Внешняя сторона карточки
    :param reverse_side: Обратная сторона карточки
    :param user_id: Пользователь (id)
    :return:
    """
    with sq.connect(bd) as con:
        cur = con.cursor()
        #
        cur.execute(f"""
        INSERT INTO memory_card (front_side, reverse_side, user_id)
        VALUES('{front_side}', '{reverse_side}', {user_id})
                """)


def check_uniq_column(name_table: str, name_column: str, check_value: str) -> True or False:
    """
    Проверяет уникальность добавляемого значения
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
        WHERE {name_column} == '{check_value}'
                """)

        for i in cur:
            check.append(i)

        if len(check) > 0:
            return False
        else:
            return True


# Проверка уникальности лицевой стороны карточки
if check_uniq_column('memory_card', 'front_side', f'{front_side}'):
    print(f'Запись "{front_side}" добавлена в {name_of_the_database} ')
    insert_memory_card(front_side, reverse_side, user_id)
else:
    print(f'Запись "{front_side}" уже есть.')


def users_item(user_id: int) -> []:
    pass


def learning_to_write():
    pass


def all_user() -> []:
    return [i[0] for i in sql_request(dc.request['users'])]


print(all_user())
