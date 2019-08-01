# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo


class IcoParserPipeline(object):

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        spider_name = spider.name
        team_collection = f'team_{spider_name}'
        team = item.get('team')
        for key, persons in team.items():
            ids = []
            for person in persons:
                result = self.db[team_collection].find_one({'profile': person.get('profile')})
                if result is not None:
                    ids.append(result.get('_id'))
                else:
                    result = self.db[team_collection].insert_one(dict(person))
                    ids.append(result.inserted_id)
            team[key] = ids
        self.db[spider_name].insert_one(dict(item))
        return item
