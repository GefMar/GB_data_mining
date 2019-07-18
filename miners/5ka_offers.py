import requests
import random
import time
import json

api_offers = 'https://5ka.ru/api/v2/special_offers/'
params = {"page": 1} 

while True:
    raw_json = requests.get(api_offers, params=params).json()

    for item in raw_json.get('results'):
        with open(f'{item.get("id")}.json', 'w') as f:
            f.write(json.dumps(item))
    
    print(f"items from page {params.get('page')} saved")

    if raw_json.get('next') is None:
        print(f"last page is {params.get('page')}")
        break

    params["page"] += 1
    
    time.sleep(random.randint(1, 2))