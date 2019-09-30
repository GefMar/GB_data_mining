# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient
from database.base import VacancyDB
from database.models import Vacancy
import scrapy
from scrapy.pipelines.images import ImagesPipeline


class JobparserPipeline(object):
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.vacancy
        self.sql_db = VacancyDB('sqlite:///vacancy.sqlite')

    def process_item(self, item, spider):
        collection = self.mongo_base[spider.name]
        collection.insert_one(item)
        # db_item = Vacancy(name=item.get('name'), spider=spider.name, salary=item.get('salary'))
        # self.sql_db.add_salary(db_item)
        return item


class AvitoPhotosPipelines(ImagesPipeline):
    def get_media_requests(self, item, info):
        pass
        if item['photos']:
            for img in item['photos']:
                try:
                    yield scrapy.Request(img)
                except Exception as e:
                    pass

    def item_completed(self, results, item, info):
        if results:
            item['photos'] = [itm[1] for itm in results if itm[0]]
        return item
