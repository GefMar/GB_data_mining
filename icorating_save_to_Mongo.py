import requests
from pymongo import MongoClient
from alchemy_orm import IcoRatingStartup
from alchemy_orm import Base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.orm import session

# Создаем клиента MongoDB
CLIENT = MongoClient('localhost', 27017)
# Выбираем базу
MONGO_DB = CLIENT.icorating_db
# Создаем коллекцию
COLLECTION = MONGO_DB.icos

engine = create_engine('sqlite:///icorating.db')
Base.metadata.create_all(engine)

db_session = sessionmaker(bind=engine)
db_session.configure(bind=engine)

# Инициируем ссылку
site_url = 'https://icorating.com/ico/all/load/?sort=name&direction=asc&page={}'

#
class ICORating:
    icos = []
    current_page = 1

    def __init__(self, url):

        last_page = self.get_data(url.format(self.current_page))['icos']['last_page']

        while True:
            if self.current_page > last_page:
                break
            else:
                data = self.get_data(url.format(self.current_page))

            for ico in data['icos']['data']:
                self.icos.append(IcoRatingStartup(**ico))

            self.current_page += 1

        COLLECTION.insert_many(self.icos)
        session = db_session()
        session.add_all(self.icos)
        session.commit()
        session.close()


    def get_data(self, url):
        return requests.get(url).json()


if __name__ == '__main__':
    collection = ICORating(site_url)
    print('Done')