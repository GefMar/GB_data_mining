import os
import requests


url = 'https://icobench.com/icos'
params = {}
r = requests.get(url, params=params)

if not os.path.isdir('ICO Pages'):
    os.mkdir('ICO Pages')

for i in range(1, 469 + 1):
    params['page'] = i
    r = requests.get(url, params=params)
    filename = str(i) + '.HTML'

    with open(f'./ICO Pages/{filename}', 'wb') as f:
        f.write(bytes(r.text, 'utf-8'))
