import requests
from pymongo import MongoClient
from alchemy_orm import New as DbNew
from alchemy_orm import Base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.orm import session

api_url = 'https://5ka.ru/api/news/'
CLIENT = MongoClient('localhost', 27017)
MONGO_DB = CLIENT.news_5ka
COLLECTION = MONGO_DB.news

engine = create_engine('sqlite:///news.db')
Base.metadata.create_all(engine)

db_session = sessionmaker(bind=engine)
db_session.configure(bind=engine)


class News5ka:
    news = []
    next = None
    previous = None

    def __init__(self, url):

        while True:
            if self.next:
                data = self.get_next_data(self.next)
            else:
                data = self.get_next_data(url)

            for item in data.get('results'):
                # self.products.append(DbProduct(**item))
                self.news.append(item)

            for key, value in data.items():
                setattr(self, key, value)

            if not data['next']:
                break
        COLLECTION.insert_many(self.news)

        session = db_session()
        session.add_all(self.news)

        session.commit()
        session.close()

    def get_next_data(self, url):
        return requests.get(url).json()


class Product:
    def __init__(self, new_dict):
        for key, value in new_dict.items():
            setattr(self, key, value)


if __name__ == '__main__':
    collection = News5ka(api_url)
    print('***')
