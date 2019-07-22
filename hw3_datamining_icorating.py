# Задание:
# С сайта icorating.com спарсить все ICO как и ранее, но сохранить все в MongoDB и SQLite (с использованием sqlalchemy)
# Усложняется задача тем что: все вложенные обьекты должны быть отдельными объектами в БД и должны сохраниться связи.

from pymongo import MongoClient
import requests
import json
from pprint import pprint


# Создание базы данных icorating и коллекции icos
client = MongoClient('mongodb://127.0.0.1:27017')
db = client['icorating']
# Удаление коллекции icos, если таковая уже есть в базе
if db.icos:
    db.icos.drop()
# Создание коллекции icos
icos = db.icos


# Получение данных о числе страниц сайта, чтобы знать, на какой странице остановиться
first_page_url = 'https://icorating.com/ico/all/load/?page=1'
first_page_data = requests.get(first_page_url)
first_page_json_data = first_page_data.json()
last_page_num = int(first_page_json_data['icos']['last_page'])
print('LAST PAGE', first_page_json_data['icos']['last_page'])

general_site_url = 'https://icorating.com/ico/all/load'

for page_num in range(1, last_page_num + 1):  #177

    params = {"page": page_num}
    site_data = requests.get(general_site_url, params)
    site_json_data = site_data.json()
    icos_json_data = site_json_data['icos']['data']

    print('status_code:', site_data.status_code) # это код, возвращаемый сервером
    print('url:', site_data.url)

    # Добавление ico-документов в коллекцию icos базы данных icorating
    for ico_data in icos_json_data:
        icos.insert_one(ico_data)

    print('page', page_num, 'is loaded\n')

print('\nDONE!')
