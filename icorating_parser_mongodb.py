import requests
from pymongo import MongoClient


icorating_api_url = 'https://icorating.com/ico/all/load/?page=1'
CLIENT = MongoClient('mongodb://127.0.0.1:27017')
ICORATING_DB = CLIENT.icorating
ICORATING_COLLECTION = ICORATING_DB.icos


class Icorating:
    icos = []
    next = None
    previous = None

    def __init__(self, url):

        while True:
            if self.next:
                data = self.get_next_data(self.next)
            else:
                data = self.get_next_data(url)

            for item in data.get('results'):
                self.icos.append(item)
                # ICORATING_COLLECTION.insert_one(item)

            for key, value in data.items():
                setattr(self, key, value)

            if not data['next']:
                break

        ICORATING_COLLECTION.insert_many(self.icos)

    def get_next_data(self, url):
        return requests.get(url).json()


if __name__ == '__main__':
    collection = Icorating(icorating_api_url)
    print('***')
