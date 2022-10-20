import bot_function
from pprint import pprint

name = ('Альберт', 'Илья', 'Фёдор', 'Боб')
profile_id = (645419280, 645419281, 645419282, 645419283)

for i in range(len(profile_id)):
    bot_function.insert_user(name[i], profile_id[i])

bot_function.insert_memory_card(f"old wive'stale", 'бабушкины сказки', profile_id[2])

itm = bot_function.users_item(profile_id[1])

pprint(len(itm))
pprint(itm)
