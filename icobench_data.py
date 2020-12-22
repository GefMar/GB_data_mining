import requests

site_url = 'https://icobench.com/icos'
first_page = 1
last_page = 469
params = {"page": []}
for i in range(first_page, last_page+1):
    params['page'] = i
    site_data = requests.get(site_url, params=params)
    tmp = site_data.text
    new_file = f"icobench_ico_page_{i}.html"
    with open(new_file, 'w', encoding='utf-8') as f:
        f.write(tmp)
