import csv
import json
import os

import requests

# https://5ka.ru/api/v2/special_offers/?store=&records_per_page=12&page=1&categories=&ordering=&price_promo__gte=&price_promo__lte=&search=
url = 'https://5ka.ru/api/v2/special_offers/'
params = {
    'store': None,
    'records_per_page': 20,
    'page': 1,
    'categories': None,
    'ordering': None,
    'price_promo__gte': None,
    'price_promo__lte': None,
    'search': None
}

# создаем папку с результатом
try:
    os.mkdir('result_5ka')
except:
    pass

res = []
num = 1
r = requests.get(url, params=params)
while r.json().get('next', False):
    # результаты по каждой странице
    filename = str(num) + '.json'
    with open('./result_5ka/' + filename, 'w') as f:
        json.dump(r.json()['results'], f, indent=4, ensure_ascii=False)

    # записываем в массив результат для общего файлв
    res.extend(r.json()['results'])

    # меняем параматры/страницу
    url = r.json().get('next', False)
    r = requests.get(url)

    num += 1

# записываем все данные в общий файл
with open('./result_5ka/' + 'all.json', 'w') as f:
    json.dump(res, f, indent=4, ensure_ascii=False)


################################## ВСЕ ДАННЫЕ В CSV ##################################

# функция фильтр
def fitered_data(
        id,
        name,
        img_link,
        date_begin,
        date_end,
        description,
        price_reg__min,
        price_promo__min, **kwargs
):
    price_reg__min = str(price_reg__min).replace('.', ',')
    price_promo__min = str(price_promo__min).replace('.', ',')
    return [id, name, img_link, date_begin, date_end, description, price_reg__min, price_promo__min]

# фильтруем и распаковываем
res_data = []
for el in res:
    data = {**el['promo'], **el['current_prices']}
    data.update(el)
    res_data.append(fitered_data(**data))

# записываем в csv
with open('./result_5ka/all.csv', 'w') as f:
    writer = csv.writer(f, delimiter=';')
    writer.writerow(['ID',
                     'Наименование',
                     'Ссылка на картинку',
                     'Начало акции',
                     'Конец акции',
                     'Описание',
                     'Цена без акции руб',
                     'Цена по акции руб'])
    for el in res_data:
        writer.writerow(el)
