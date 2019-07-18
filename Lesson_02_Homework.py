import requests


def write_to_html(html, page):
    path = f'html_data_out/icobench_ico_page_{page}.html'
    file_html = open(path, 'a', encoding='utf-8')
    file_html.write(html)
    file_html.close


site_url = 'https://icobench.com/icos'
site_data = requests.get(site_url)
print(site_data.headers)

stop_word = "We don't have the information about this ICO yet"
page = 294
while True:
    params = {'page': page}
    site_data = requests.get(site_url, params=params)

    if site_data.text.find(stop_word) == -1:
        write_to_html(site_data.text, page)
        page += 1

    else:
        break
