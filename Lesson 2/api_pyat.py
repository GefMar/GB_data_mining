import requests
import time
import random
import json

api_pyat = 'https://5ka.ru/api/v2/special_offers/?store=&records_per_page=12&page=1&categories=&ordering=&price_promo__gte=&price_promo__lte=&search='

while True:
    api_data_pyat = requests.get(api_pyat)
    res_json = api_data_pyat.json()

    for item in res_json.get('results'):
        item_json = json.loads(item)
        with open(f'{item_json.get("id")}.json', 'w', encoding='utf-8') as f:
            f.write(item)

    if res_json.get('next') is None:
        break
    else:
        api_pyat = res_json.get('next')
        time.sleep(random.randint(1, 5))
