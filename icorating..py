import requests
import random
import time
import os

try:
    os.mkdir('data_icorating')
except:
    pass
sate_url = 'https://icorating.com/ico/all/load/'
params = {'page':1}
sate_data = requests.get(sate_url, params=params)
while params["page"]<177:
    sate_data = requests.get(sate_url, params=params)
    with open(f'data_icorating/icorating_page_{params["page"]}.html', 'w') as file:
        file.write(sate_data.text)
    params["page"] += 1
    time.sleep(random.randint(1, 5))
    print (params["page"]) 
