from pprint import pprint
import httplib2
import apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials

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
    coll_list_value = []

    values = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id,
        range=f'{coll}{row_1}:{coll}{row_2}',
        majorDimension='COLUMNS'
    ).execute()

    for i in values['values']:
        for cell_value in i:
            coll_list_value.append(cell_value)

    return coll_list_value



