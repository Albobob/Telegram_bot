import bot_function
from pprint import pprint

name = ('Альберт', 'Илья', 'Фёдор', 'Боб')
profile_id = (645419280, 645419281, 645419282, 645419283)

for i in range(len(profile_id)):
    bot_function.insert_user(name[i], profile_id[i])

bot_function.insert_memory_card(f"tale", 'сказка', profile_id[2])

print(bot_function.get_memory_card(profile_id[0], 1))
