# Задание 1: Ресурс https://icobench.com/icos
# Необходимо выгрузить в отдельные файлы html код каждой страницы каталога ICO проектов. Шаблон имени файла icobench_ico_page_{номер страницы}.html

import requests

site_url = "https://icobench.com/icos"
folder_name = "icobench.com"
page_count = 470
url_params = {"page": 0}

for page_number in range(1, page_count + 1):
	url_params["page"] = page_number

	site_data = requests.get(site_url, url_params)
	site_data.request

	if site_data.status_code == 200:
		try:
			path = '{0}\\icobench_ico_page_{1}.html'.format(folder_name, page_number)
			f = open(path, 'w', encoding='utf-8')
			f.write(site_data.text)
			f.close()
			file_result = "OK"
		except Exception:
			file_result = "Error"

	print('{0}. Status: {1} Write: {2}'.format(page_number, site_data.status_code, file_result))
