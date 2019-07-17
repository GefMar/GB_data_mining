import requests
import json

ico_url = 'https://icorating.com/ico/all/load/'

param = {"page": []}
first_page = 1
last_page = 176

for i in range(first_page, last_page+1):
    param['page'] = i
    ico_data = requests.get(ico_url, params=param).text
    data = json.loads(ico_data)
    try:
        for j in range(30):
            tmp = data['icos']['data'][j]
            id = data['icos']['data'][j]['id']
            new_file = f"{id}_ico.json"
            with open(new_file, 'w', encoding='utf-8') as f:
                json.dump(tmp, f)
    except: print("The End.")




