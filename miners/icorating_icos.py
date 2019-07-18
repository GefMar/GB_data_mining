import requests
import random
import time
import json

api_icos = 'https://icorating.com/ico/all/load/'
params = {"page": 1} 

while True:
    raw_json = requests.get(api_icos, params=params).json()
    json_icos = raw_json.get('icos')

    if json_icos.get('current_page') > json_icos.get('last_page'):
        print(f"last page is {params.get('page') - 1}")
        break

    for item in json_icos.get('data'):
        with open(f'{item.get("id")}.json', 'w') as f:
            f.write(json.dumps(item))
    
    print(f"items from page {params.get('page')} saved")
    params["page"] += 1
    time.sleep(random.randint(1, 2))