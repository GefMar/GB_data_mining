import os

import requests

# https://icobench.com/icos?page=2
url = 'https://icobench.com/icos'
params = {}

# создаем папку с результатами
try:
    os.mkdir('result_iconech')
except:
    pass

for i in range(1, 469 + 1):
    params['page'] = i
    r = requests.get(url, params=params)
    filename = str(i) + '.html'
    with open('./result_iconech/' + filename, 'wb') as f:
        f.write(r.raw.read())

    if i % 10 == 0: print(i) # показывает статус каждого 10 страницы
print('Complite!')
