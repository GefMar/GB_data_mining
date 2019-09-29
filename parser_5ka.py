import requests
from pymongo import MongoClient
from alchemy_orm import Product as DbProduct
from alchemy_orm import Base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.orm import session

api_url = 'https://5ka.ru/api/v2/special_offers/?records_per_page=12&page=1'
CLIENT = MongoClient('localhost', 27017)
MONGO_DB = CLIENT.special5ka2
COLLECTION = MONGO_DB.products

engine = create_engine('sqlite:///products.db')
Base.metadata.create_all(engine)

db_session = sessionmaker(bind=engine)
db_session.configure(bind=engine)


class Special5ka:
    products = []
    next = None
    previous = None

    def __init__(self, url):

        while True:
            if self.next:
                data = self.get_next_data(self.next)
            else:
                data = self.get_next_data(url)

            for item in data.get('results'):
                self.products.append(DbProduct(**item))
                # self.products.append(item)

            for key, value in data.items():
                setattr(self, key, value)

            if not data['next']:
                break
        # COLLECTION.insert_many(self.products)
        session = db_session()
        session.add_all(self.products)
        session.commit()
        session.close()

    def get_next_data(self, url):
        return requests.get(url).json()


class Product:
    def __init__(self, product_dict):
        for key, value in product_dict.items():
            setattr(self, key, value)


if __name__ == '__main__':
    collection = Special5ka(api_url)
    print('***')
