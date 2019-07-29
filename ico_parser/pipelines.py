# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient

CLIENT = MongoClient('localhost', 27017)
MONGO_DB = CLIENT.ico
COLLECTION = MONGO_DB.icobench
PEOPLE = MONGO_DB.people


class IcoParserPipeline(object):
    def process_item(self, item, spider):
        # if isinstance(item, IcoParserItem):
        _ = COLLECTION.insert_one(item)
        return item

# class IcoParserPeoplePipeline(object):
#     def process_item(self, item, spider):
#         if isinstance(item, IcoParserPeople):
#             _ = PEOPLE.insert_one(item)
#         return item