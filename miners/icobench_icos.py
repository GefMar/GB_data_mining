import requests
import random
import time

url = 'https://icobench.com/icos'
params = {"page": 1}

while True:
    page = requests.get(url, params=params)
    if 'class="no_data"' in page.text:
        print(f"last page is {params.get('page') - 1}")
        break
    with open(f'icobench_ico_page_{params["page"]}.html', 'w') as f:
        f.write(page.text)
        print(f"page {params.get('page')} saved")
    params["page"] += 1
    time.sleep(random.randint(1, 2))
