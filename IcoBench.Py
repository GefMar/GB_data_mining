import requests


def to_file(html, page):
    path = f'html_data_out/icobench_ico_page_{page}.html'
    f_html = open(path, 'a', encoding='utf-8')
    f_html.write(html)
    f_html.close


url = 'https://icobench.com/icos'
data = requests.get(url)
page = 1
stop = "We don't have the information about this ICO yet"


print(data.headers)

while True:
    params = {'page': page}
    data = requests.get(url, params=params)

    if data.text.find(stop) == -1:
        to_file(data.text, page)
        page += 1
    else:
        break
