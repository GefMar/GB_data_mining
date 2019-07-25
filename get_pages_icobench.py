import requests
import time
import random
import os

# Создаем ссылку
site_url = 'https://icobench.com/icos'
# Инициируем параметры ссылки
params = {'page': 1}

# Т.к. файлов слишком много решил сложить их в отдельную папку
my_path = 'icobench_pages/'
# Если папки не существует, то создать ее
if not os.path.isdir(my_path):
    os.mkdir(my_path)

# Цикл по сохранению кода страниц
for i in range(1, 470):
    # Присваиваем номер страницы
    params['page'] = i
    time.sleep(random.randint(1, 2))
    # Делаем запрос к странице
    site_data = requests.get(site_url, params=params)
    # Открываем файл на запись
    with open(f'icobench_pages/icobench_ico_page_{i}.html', 'w') as page:
        # Сохраняем текст запрошенной страницы в файл
        page.write(site_data.text)
