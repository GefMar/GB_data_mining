import requests
import json
from pymongo import MongoClient
from alchemy_orm import ICO
from alchemy_orm import Base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.orm import session

api_url = 'https://icorating.com/ico/all/load/?page={}&sort=investment_rating&direction=desc'

engine = create_engine('sqlite:///icoratingdb.db')
Base.metadata.create_all(engine)
engine.execute('DELETE FROM ico_info')
db_session = sessionmaker(bind=engine)
db_session.configure(bind=engine)

client = MongoClient('192.168.126.134', 27017)
db = client.icoratingdb
# очистить коллекцию перед началом
db.drop_collection('icos')
collection = db.icos

class ICOrating_Parser:
    icos = []
    current_page = None
    last_page = None

    def __init__(self, url):
    	
    	self.current_page = 1
    	
    	while True:
            if self.current_page == 3:
                break
            else:
                print('Current page: {}'.format(self.current_page))
                data = self.get_next_data(url.format(self.current_page))
            
            for item in data['icos'].get('data'):
                self.icos.append(ICO(**item))

            result = collection.insert_many(data['icos']['data'])
            print('Inserted {} items into MongoDb'.format(len(result.inserted_ids)))

            self.current_page = data['icos']['current_page'] + 1
            self.last_page    = data['icos']['last_page']

    	session = db_session()
    	session.add_all(self.icos)
    	session.commit()
    	session.close()

    def get_next_data(self, url):
        return requests.get(url).json()

if __name__ == '__main__':
    ICOrating_Parser(api_url)
    print("Done")