import requests
import time
import random

site_url = 'https://icobench.com/icos'
params = {"page": 1}

while True:
    site_data = requests.get(site_url, params=params)
    if site_data.text.find("We don't have the information about this ICO yet.") != -1:
        break
    with open(f'icobench_ico_page_{params["page"]}.html', 'w', encoding='utf-8') as f:
        f.write(site_data.text)
    params["page"] += 1
    if params["page"] % 3 == 0:
        time.sleep(random.randint(1, 5))
