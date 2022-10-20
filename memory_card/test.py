import bot_function

name = ('Альберт', 'Илья', 'Фёдор', 'Боб')
profile_id = (645419280, 645419281, 645419282, 645419283)

for i in range(len(profile_id)):
    bot_function.insert_user(name[i], profile_id[i])

bot_function.insert_memory_card('wrong', 'неправильный', profile_id[0])
