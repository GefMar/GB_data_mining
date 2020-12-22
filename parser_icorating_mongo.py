import requests
from pymongo import MongoClient
import time


api_url = ' https://icorating.com/ico/all/load/?page=1'
CLIENT = MongoClient('localhost', 27017)
CLIENT.drop_database('Icos')
MONGO_DB = CLIENT.Icos
COLLECTION = MONGO_DB.icoscoll


class Icorating:
    icoscoll = []

    def __init__(self, url):
        first_page = 1
# page=0 и page=1 на сайте дублируются, поэтому начинаем с 1.
        last_page = self.get_data(url, 1).get('icos').get('last_page')

        for i in range(first_page, last_page+1):
            time.sleep(1)
            ico_data = self.get_data(url, i)

            for item in ico_data.get('icos').get('data'):
                self.icoscoll.append(item)

            for key, value in ico_data.items():
                setattr(self, key, value)

        COLLECTION.insert_many(self.icoscoll)

    def get_data(self, url, i):
        data_site = requests.get(url, params={"page": i})

        return data_site.json()


if __name__ == '__main__':
    collection = Icorating(api_url)
    print('**The End.**')