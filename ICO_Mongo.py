import requests
from pymongo import MongoClient

api_url = 'https://icorating.com/ico/all/load/'

CLIENT = MongoClient('localhost', 27017)
MONGO_DB = CLIENT.icorating
COLLECTION = MONGO_DB.ico


class Icorating:
    icos_data = []
    last = None

    def __init__(self, url):
        params = {"page":1}

        while True:
            if self.last:
                params["page"] += 1
                data = self.get_next_data(url, params)
            else:
                data = self.get_next_data(url, params)
                self.last = data.get('icos').get('last_page')

            for item in data.get('icos').get('data'):
                self.icos_data.append(item)

            if data.get('icos').get('current_page') == self.last:
                break

        COLLECTION.insert_many(self.icos_data)

    def get_next_data(self, url, params):
        return requests.get(url, params).json()



if __name__ == '__main__':
    collection = Icorating(api_url)
    print('***')
