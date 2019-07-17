import requests
site_url = 'https://icobench.com/icos'
for i in range(1,469):
    params = {'page': "1"}
    params['page'] = i
    site_data = requests.get(site_url, params=params)
    x = str(i)
    f = open('icobench_ico_page_'+ x +'.html', 'w', encoding = 'utf-8')
    f.write(site_data.text)
    f.close
