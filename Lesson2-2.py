import requests
import json


ico_rating_url = "https://icorating.com/ico/all/load/"
params = {"page": 1}
file_name_all = "icorating/icorating_ico_"

for i in range(1, 177):
    params["page"] = i
    page_data = requests.get(ico_rating_url, params=params)
    page_json = page_data.json()
    page_json = page_json.get('icos')
    page_json = page_json.get('data')
    for ico in page_json:
        file_name = file_name_all + str(ico.get('id')) + ".json"
        with open(file_name, "w", encoding="utf-8") as f:
            f.write(json.dumps(ico))


