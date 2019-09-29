import requests
from pymongo import MongoClient
from alchemy_orm import Product as DbProduct
from alchemy_orm import Base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.orm import session

api_url = 'https://icorating.com/ico/all/load/'

engine = create_engine('sqlite:///products.db')
Base.metadata.create_all(engine)

db_session = sessionmaker(bind=engine)
db_session.configure(bind=engine)


class Icorating:
    products = []
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
                self.products.append(DbProduct(**item))

            if data.get('icos').get('current_page') == self.last:
                break
                
        session = db_session()
        session.add_all(self.products)

        session.commit()
        session.close()

    def get_next_data(self, url, params):
        return requests.get(url, params).json()


if __name__ == '__main__':
    collection = Icorating(api_url)
    print('***')
