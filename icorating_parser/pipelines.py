# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from pymongo import MongoClient
import requests
import hashlib
import os
import urllib3


class IcoParserPipeline(object):
    client = None
    db = None

    def open_spider(self, spider):
        self.client = MongoClient('192.168.126.134', 27017)
        self.db = self.client.icodb
        # очистить коллекции перед началом
        self.db.drop_collection(spider.name)
        self.db.drop_collection('persons')
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        # print('============BEGIN ITEM=============')
        # print(item)

        # Download whitepaper
        if spider.name == 'icobench' and item['whitepaper']:
            item['whitepaper'] = self.download_whitepaper(item['whitepaper'])

        # Replace person name with person ID
        if spider.name == 'icobench':
            for i in range(0, len(item['team'])):
                item['team'][i]['_id'] = self.get_or_create_person(item['team'][i].copy())
                item['team'][i].pop('name')
                item['team'][i].pop('socials')

        # Insert into MongoDB
        self.db[spider.name].insert_one(item)

        # print('============END ITEM=============')
        return item

    def get_or_create_person(self, person):
        id = self.db['persons'].find_one({"name": person['name']})
        if id:
            return id.get('_id')
        else:
            person.pop('position')
            id = self.db['persons'].insert_one(person).inserted_id
            return id

    def download_whitepaper(self, link) -> str:
        hash = hashlib.md5(link.encode('utf-8')).hexdigest()
        path = os.getcwd() + '/data/' + hash + '.pdf'
        try:
            r = requests.get(link, verify=False)
            if r.headers.get('Content-Type', '!NO Content-Type KEY!') != 'application/pdf':
                raise requests.exceptions.ConnectionError()
            open(path, 'wb').write(r.content)
            return path
        except (requests.exceptions.ConnectionError, requests.exceptions.InvalidSchema, requests.exceptions.MissingSchema):
            print('Whitepaper {} is not available. Keeping original link in database.'.format(link))
            return link
