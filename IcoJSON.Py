import json
import os
import requests


if not os.path.isdir('ICO JSON Docs'):
    os.mkdir('ICO JSON Docs')

url = 'https://icorating.com/ico/all/load'
params = {'sort': 'name', 'direction': 'asc', 'page': 1}
data = requests.get(url, params=params)
data_json = data.json()
last_page = data_json['icos']['last_page']

for i in range(1, last_page + 1):
    params['page'] = i
    data = requests.get(url, params=params)
    data_json = data.json()['icos']['data']

    for project in data_json:
        p_id = project.get('id')
        p_data = json.dumps(project)

        with open(f'./ICO JSON Docs/{p_id}.JSON', 'wb') as f:
            f.write(bytes(p_data, 'utf-8'))
