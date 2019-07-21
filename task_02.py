# Задание 2: Ресурс https://5ka.ru/special_offers/ 
# Необхоидмо выгрузить все товары по акции - каждый товар в отдельный файл (csv или json), имя файла id товара, выгрузить необходимо абсолютно все товары по акции которые есть в источнике.

import json
import requests

folder_name = "5ka.ru"
site_url = "https://5ka.ru/api/v2/special_offers?page=1"

while site_url != None:

	site_data = requests.get(site_url)
	site_data.request

	products = site_data.json().get('results')

	for product in products:
		file_name = product["id"]
		file_path = '{0}\\{1}.json'.format(folder_name, file_name)

		with open(file_path, 'w') as file:
			json.dump(product, file, indent = 4)

	site_url = site_data.json().get('next')

print("the end")
