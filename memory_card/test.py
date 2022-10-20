import bot_function
from pprint import pprint

name = ('Альберт', 'Илья', 'Фёдор', 'Боб', 'Кирилл')
profile_id = (645419280, 645419281, 645419282, 645419283, 645419284)

for i in range(len(profile_id)):
    bot_function.insert_user(name[i], profile_id[i])

bot_function.insert_memory_card(f"response", 'ответ', profile_id[4])

bot_function.learning_to_write(profile_id[4], 10)
# pprint(bot_function.users_item(profile_id[4]))