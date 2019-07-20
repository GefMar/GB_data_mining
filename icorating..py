import requests
import random
import time
import json
from pymongo import MongoClient


sate_url = 'https://icorating.com/ico/all/load/'
CLIENT = MongoClient('localhost', 27017)
MONGO_DB = CLIENT.ico_project
COLLECTION = MONGO_DB.ico_name


class icorating:
    params = {'page':1}
    info_data = []
    def __init__(self, url):        
        while True:
            data = self.sate_data(url, self.params)
            dt = data.get('icos')['data']            
            data_dict = data.get('icos')            
            
            for i in dt:
                self.info_data.append(i)
            with open (f'data_icorating/test.json','w') as file:
                json.dump(self.info_data, file, sort_keys=True, indent=4)
            if self.params['page'] == 1:
                break

            time.sleep(random.randint(1,5))
            self.params['page'] +=1

        COLLECTION.insert_many(self.info_data)

    def sate_data(self, url, params):
        return requests.get(sate_url, params=params).json()
        
if __name__ == '__main__':
    conect = icorating(sate_url)
    print("Finish")