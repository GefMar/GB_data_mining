import requests
from pymongo import MongoClient
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.orm import session

# Создаем клиента MongoDB
CLIENT = MongoClient('localhost', 27017)
# Выбираем базу
MONGO_DB = CLIENT.icorating_db
# Создаем коллекцию
COLLECTION = MONGO_DB.ico_startup

engine = create_engine('sqlite:///icorating.db')

# Инициируем ссылку
site_url = 'https://icorating.com/ico/all/load/'
# Определяем параметры. Сортировка нужна для того чтобы одни и теже проекты не попадали на разные
# страницы и не перезатирались
params = {'sort': 'name', 'direction': 'asc', 'page': 1}
# Получаем первую ссылку для получения количества страниц
site_data = requests.get(site_url, params=params)
site_data_json = site_data.json()
# Узнаем общее количество страниц
last_page = site_data_json['icos']['last_page']

# Запускаем цикл с перебором страниц
for page in range(1, last_page + 1):
    # Меняем номер страницы
    params['page'] = page
    site_data = requests.get(site_url, params=params)
    site_data_json = site_data.json()['icos']['data']
    # Перебираем все элементы в списке проектов на текущей странице
    for startup in site_data_json:
        # Сохраняем в базу
        COLLECTION.insert_one(startup)
