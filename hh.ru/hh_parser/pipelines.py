# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from pymongo import MongoClient

CLIENT = MongoClient('localhost', 27017)
MONGO_DB = CLIENT.hh


class HhParserPipeline(object):
    project_collection = MONGO_DB.hh_collection

    def process_item(self, item, spider):
        _ = self.project_collection.insert_one(item)
        return item
