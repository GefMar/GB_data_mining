# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from pymongo import MongoClient

client = MongoClient('192.168.126.134', 27017)
db = client.icoratingdb
# очистить коллекцию перед началом
db.drop_collection('icos')
collection = db.icos


class IcoratingParserPipeline(object):
    def process_item(self, item, spider):
        collection.insert_one(item)
        return item
