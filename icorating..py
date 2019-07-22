import requests
import random
import time
import json
from pymongo import MongoClient
from alchemy_orm import ico_base as DbICO
from alchemy_orm import Base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.orm import session



sate_url = 'https://icorating.com/ico/all/load/'
CLIENT = MongoClient('localhost', 27017)
MONGO_DB = CLIENT.ico_project
COLLECTION = MONGO_DB.ico_name

engine = create_engine('sqlite:///ICO_info.db')
Base.metadata.create_all(engine)

db_session = sessionmaker(bind=engine)
db_session.configure(bind=engine)



class icorating:
    params = {'page':1}
    info_data = []
    def __init__(self, url):        
        while True:
            data = self.sate_data(url, self.params)
            dt = data.get('icos')['data']          
                      
            
            for i in dt:
                self.info_data.append(DbICO(**i))
                #self.info_data.append(i)                
#            with open (f'data_icorating/test.json','w') as file:
#                json.dump(self.info_data, file, sort_keys=True, indent=4)
            if self.params['page'] == 1:
                break

            time.sleep(random.randint(1,5))
            self.params['page'] +=1

        #COLLECTION.insert_many(self.info_data)

        session = db_session()
        session.add_all(self.info_data)

        session.commit()
        session.close()


    def sate_data(self, url, params):
        return requests.get(sate_url, params=params).json()
        
if __name__ == '__main__':
    conect = icorating(sate_url)
    print("Finish")