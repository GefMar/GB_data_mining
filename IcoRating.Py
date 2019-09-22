import random
import requests
import time
from pymongo import MongoClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from alchemy_orm import Base
from alchemy_orm import ICOBase


url = 'https://icorating.com/ico/all/load'
CLIENT = MongoClient('localhost', 27017)
MONGO_DB = CLIENT.ICO
COLLECTION = MONGO_DB.ICO_Name

engine = create_engine('sqlite:///ICOBase.db')
Base.metadata.create_all(engine)

db_session = sessionmaker(bind=engine)
db_session.configure(bind=engine)


class ICORating:
    params = {'page': 1}
    info_data = []

    def __init__(self, url):
        while True:
            data = self.get_data(url, self.params)
            data_json = data.get('icos')['data']

            for i in data_json:
                self.info_data.append(ICOBase(**i))
                print(i)

            if self.params['page'] == 1:
                break

            time.sleep(random.randint(1, 5))
            self.params['page'] += 1

        session = db_session()
        session.add_all(self.info_data)

        session.commit()
        session.close()

    def get_data(self, url, params):
        return requests.get(url, params=params).json()


if __name__ == '__main__':
    con = ICORating(url)
    print('Done')
