# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient
from ico_parser.items import IcoParserItem, PersonItem, IcoRatingItem

CLIENT = MongoClient('localhost', 27017)
MONGO_DB = CLIENT.ico


class IcoParserPipeline(object):
    COLLECTION = MONGO_DB.icobench
    def process_item(self, item, spider):
        if (isinstance(item, IcoParserItem)):
            _ = self.COLLECTION.insert_one(item)
        return item

class PersonPipeline(object):
    COLLECTION = MONGO_DB.persons
    def process_item(self, item, spider):
        if (isinstance(item, PersonItem)):
            if not self.COLLECTION.find_one(item):
                _ = self.COLLECTION.insert_one(item)
        return item

class IcoRatingPipeline(object):
    COLLECTION = MONGO_DB.icorating
    def process_item(self, item, spider):
        if (isinstance(item, IcoRatingItem)):
            _ = self.COLLECTION.insert_one(item)
        return item