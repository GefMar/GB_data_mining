import requests
from pymongo import MongoClient
from alchemy_orm import Company as DbCompany
from alchemy_orm import Base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.orm import session

api_url = 'https://icorating.com/ico/all/load/'

CLIENT = MongoClient('localhost', 27017)
# MONGO_DB = CLIENT.ico
MONGO_DB = CLIENT['ico']
COLLECTION = MONGO_DB.companies

engine = create_engine('sqlite:///companies.db')
Base.metadata.create_all(engine)
db_session = sessionmaker(bind=engine)
db_session.configure(bind=engine)



class ico_grab:
    companies = []

    def __init__(self, url):

        data = self.get_data(url)

        for item in data['icos']['data']:
            self.companies.append(DbCompany(**item))

        for key, value in data.items():
            setattr(self, key, value)

        COLLECTION.insert_many(data['icos']['data'])

        session = db_session()
        session.add_all(self.companies)
        session.commit()
        session.close()

    def get_data(self, url):
        # param_page = f"store=&records_per_page=1&page={i}"
        param_page = ''

        site_data = requests.get(api_url, params=param_page)
        return site_data.json()


class Ico:
    def __init__(self, ico_dict):
        for key, value in ico_dict.items():
            setattr(self, key, value)

if __name__ == '__main__':
    collection = ico_grab(api_url)
    print('***')