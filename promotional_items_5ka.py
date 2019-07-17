import requests
import random
import time

sate_url = 'https://5ka.ru/special_offers/'
params = {'page':1}
sate_data = requests.get(sate_url, params=params)
while params["page"]<470:
    sate_data = requests.get(sate_url, params=params)
    with open(f'data_ico_bench/icobench_ico_page_{params["page"]}.html', 'wb') as file:
        file.write(sate_data.text.encode('UTF-8'))
    params["page"] += 1
    time.sleep(random.randint(1, 5))
    print (params["page"]) 
