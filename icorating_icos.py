import requests
import random
import time

from pymongo import MongoClient

from alchemy_orm import Base
from alchemy_orm import IcoItem
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

api_url = 'https://icorating.com/ico/all/load/'

class Icorating:
    icos = []

    def __init__(self, url):
        
        params = {"page": 176}

        while True:
            raw_json = self.get_next_data(url, params)
            json_icos = raw_json.get('icos')

            if json_icos.get('current_page') > json_icos.get('last_page'):
                print(f"last page is {params.get('page') - 1}")
                break

            for item in json_icos.get('data'):
                self.icos.append(item)
            
            print(f"items from page {params.get('page')} saved")
            params["page"] += 1
            time.sleep(random.randint(1, 2))

    def get_next_data(self, url, params):
        return requests.get(url, params=params).json()

    def get_icos_obj(self):
        icos = []
        for item in self.icos:
            icos.append(IcoItem(**item))
        return icos


class Storage:
    mongo_client = None

    def __init__(self):
        self.mongo_client = MongoClient('192.168.0.202', 27017)
    
    def save_to_mongo(self, db_name, collection, data):
        self.mongo_client[db_name][collection].insert_many(data)

    def save_to_sql(self, data):
        engine = create_engine('sqlite:///dumps/sqlite_data.db')
        Base.metadata.create_all(engine)
        db_session = sessionmaker(bind=engine)
        db_session.configure(bind=engine)
        session = db_session()
        session.add_all(data)
        session.commit()
        session.close()

if __name__ == '__main__':
    storage = Storage()
    collection = Icorating(api_url)
    storage.save_to_sql(collection.get_icos_obj())
    storage.save_to_mongo('icos', 'items', collection.icos)
    