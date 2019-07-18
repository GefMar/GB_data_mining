import requests
import json

url = 'https://5ka.ru/api/v2/special_offers/?'

next_el = True
i = 1
while next_el:

    print("NEWPAGE=",i)
    param_page = f"store=&records_per_page=1&page={i}"

    site_data = requests.get(url,params=param_page)
    el = site_data.json()
    print(el['results'][0])
    id = el['results'][0]['id']
    # my_file = open(f"{id}.json", "w")
    # my_file.write()
    # my_file.close()

    with open(f"{id}.json", "w") as write_file:
        json.dump(el['results'][0], write_file)

    i = i+1
    # if (type(el['next']) == types.NoneType):
    # if (isinstance(type(el['next']), type(None))):
    # if (el['next'] == None):
    # if ("http" not in el['next']):
    #     next_el is False

