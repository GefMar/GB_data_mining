import requests
from pymongo import MongoClient
from ico_alchemy_orm import Ico as DbIco
from ico_alchemy_orm import Base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.orm import session

api_url = 'https://icorating.com/ico/all/load/'

CLIENT = MongoClient('localhost', 27017)
MONGO_DB = CLIENT.ico_rating
COLLECTION = MONGO_DB.ico_list

engine = create_engine('sqlite:///ico_rating.db')
Base.metadata.create_all(engine)

db_session = sessionmaker(bind=engine)
db_session.configure(bind=engine)


class ParseIco:
    ico_list = []

    def __init__(self, url):
        params = {"page": 1}

        while True:
            data = self.get_next_data(url, params)

            if data.get('icos').get('current_page') > data.get('icos').get('last_page'):
                print('Last page reached')
                break

            print('Parsing page: ' + str(params['page']))
            params["page"] += 1

            #for key, value in data.items():
                # setattr(self, key, value)

            for item in data.get('icos').get('data'):
                self.ico_list.append(DbIco(**item))
                # self.products.append(item)
            COLLECTION.insert_many(data.get('icos').get('data'))

        my_session = db_session()
        my_session.add_all(self.ico_list)
        my_session.commit()
        my_session.close()

    def get_next_data(self, url, params):
        return requests.get(url, params=params).json()


if __name__ == '__main__':
    collection = ParseIco(api_url)
    print('***')
