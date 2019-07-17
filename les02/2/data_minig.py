import requests
site_url = 'https://icorating.com/ico/'
api_site = 'https://icorating.com/ico/load/?page=1'
api_data = requests.get(api_site)
tmp_data = api_data.json()
j = tmp_data['icos']['last_page']
for i in range(1, j+1):
    print(api_site)
    for x in range(0, len(tmp_data['icos']['data'])):
        f = open(str(tmp_data['icos']['data'][x]['id']) + '.json', 'w')
        data = str(tmp_data['icos']['data'][x])
        f.write(data)
        f.close
        print(x)
    page = str(i+1)
    api_site = 'https://icorating.com/ico/load/?page=' + page
    api_data = requests.get(api_site)
    tmp_data = api_data.json()
