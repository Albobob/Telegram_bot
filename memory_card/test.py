import bot_function

name = ('Альберт', 'Илья', 'Фёдор', 'Боб')
profile_id = (645419280, 645419281, 645419282, 645419283)

for i in range(len(profile_id)):
    bot_function.insert_user(name[i], profile_id[i])

    # if bot_function.check_uniq_column('users', 'id_profile', profile_id[i]):
    #
    #     pass
    # else:
    #     print(f'Пользователь {name[i]} ({profile_id[i]}) уже имеется в {bot_function.name_of_the_database}')
