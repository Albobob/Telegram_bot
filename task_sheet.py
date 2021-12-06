from pprint import pprint
import httplib2
import apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials

user_id_ls = {645419280: 'Симонян А.Р.',
              202383142: 'Криушин Д.С.'}

# Файл, полученный в Google Developer Console
CREDENTIALS_FILE = 'creds.json'
# ID Google Sheets документа (можно взять из его URL)
spreadsheet_id = '1uL4awCgqRVeny-zRZhtwx7P5NIlq5hBxyrAEJqlmhjw'

# Авторизуемся и получаем service — экземпляр доступа к API
credentials = ServiceAccountCredentials.from_json_keyfile_name(
    CREDENTIALS_FILE,
    ['https://www.googleapis.com/auth/spreadsheets',
     'https://www.googleapis.com/auth/drive'])
httpAuth = credentials.authorize(httplib2.Http())
service = apiclient.discovery.build('sheets', 'v4', http=httpAuth)


# Пример чтения файла


def value_coll(coll, row_1, row_2):
    name_c = []

    values = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id,
        range=f'{coll}{row_1}:{coll}{row_2}',
        majorDimension='COLUMNS'
    ).execute()

    # pprint(values)
    # print(type(values))

    for i in values['values']:
        for cell_value in i:
            name_c.append(cell_value)

    return name_c


name_1_coll = (value_coll('C', 4, 1600))
name_2_coll = (value_coll('D', 4, 1600))
name_3_coll = (value_coll('E', 4, 1600))
status_coll = (value_coll('F', 4, 1600))
task_coll = (value_coll('B', 4, 1600))


# pprint(len(task_coll))
# pprint(len(name_1_coll))


def active_task(coll_date, status_coll, task_coll):
    bd_task = []
    bd_task.clear()

    for i in range(len(task_coll)):
        x = {'task': {}}

        if status_coll[i] != 'Передано в др. службу' and status_coll[i] != 'Выполнено':
            x['task']['status'] = status_coll[i]
            x['task']['name'] = coll_date[i]
            x['task']['task_value'] = task_coll[i]

            bd_task.append(x)

    return bd_task


task_1 = active_task(name_1_coll, status_coll, task_coll)
task_2 = active_task(name_2_coll, status_coll, task_coll)
task_3 = active_task(name_3_coll, status_coll, task_coll)


# pprint(task_1)

def username_task(tsk):
    tsk_nm = {}
    for itm in tsk:
        username = itm['task']['name']
        user_task = itm['task']['task_value']

        # print(f'{user_task} - {username}')
        tsk_nm[f'{user_task}'] = f'{username}'

    return tsk_nm


def get_task(user_name, tsk):
    task_list = []
    task_list.clear()

    for i in username_task(tsk):
        name = username_task(tsk)[i]
        if name == f'{user_name}':
            task_list.append(i)
            # print(i)

    return task_list


def push_task(user_id):
    name = user_id_ls.get(user_id)
    a = get_task(f'{name}', task_1)
    b = get_task(f'{name}', task_2)
    c = get_task(f'{name}', task_3)

    push_value = a + b + c

    return push_value

# user_id_ls = {645419280: 'Симонян А.Р.'}
# pprint(push_task(645419280))
