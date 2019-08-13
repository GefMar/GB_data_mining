import requests
import json
import os

# Т.к. файлов слишком много решил сложить их в отдельную папку
my_path = 'icorating_startup/'
if not os.path.isdir(my_path):
    # Если папки не существует, то создать ее
    os.mkdir(my_path)

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
        # Получаем id проекта для имени файла
        startup_id = startup.get('id')
        # Преобразовываем словарь в строку
        startup_data = json.dumps(startup)
        # Открываем файл на запись
        with open(f'icorating_startup/{startup_id}.json', 'w') as file:
            # Сохраняем в файл
            file.write(startup_data)
