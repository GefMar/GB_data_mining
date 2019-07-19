import requests
import random
import time
import os
import json

try:
    os.mkdir('data_icorating')
except:
    pass
sate_url = 'https://icorating.com/ico/all/load/'



class icorating:
    params = {'page':1}

    def __init__(self, url):        
        while True:
            data = self.sate_data(url, self.params)
            last_page = data.get('icos')['last_page']
            with open(f'data_icorating/icorating_page_{self.params["page"]}.json', 'w') as file:
                json.dump(data, file)
            data_dict = data.get('icos')
            if self.params['page'] == last_page:
                break
            self.params['page'] +=1



    def sate_data(self, url, params):
        return requests.get(sate_url, params=params).json()
        
if __name__ == '__main__':
    conect = icorating(sate_url)
    print("Finish")