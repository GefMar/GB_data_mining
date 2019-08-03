# -*- coding: utf-8 -*-
import requests

# from alchemy_orm import Company as DbCompany
# from alchemy_orm import Base
# from sqlalchemy.orm import sessionmaker
# from sqlalchemy import create_engine
# from sqlalchemy.orm import session

import scrapy
from ico_parser.items import IcoParserItem, PersonItem
from pymongo import MongoClient
import re
from time import sleep


CLIENT = MongoClient('localhost', 27017)
MONGO_DB = CLIENT.ico
COLLECTION = MONGO_DB.icorating

api_url = 'https://icorating.com/ico/all/load/'
url = 'https://icorating.com/ico/'
companies_links = []

class ico_grab:
    companies_links = []

    def __init__(self, url):
        # for i in range(176, 177):
        i = 175
        next_page = True
        while next_page is True:
            data = self.get_data(api_url, i)
            # print(i, len(data['icos']['data']))
            if len(data['icos']['data']) == 0:
                next_page = False
            else:
                for item in data['icos']['data']:
                    link = item["link"]
                    # link = link.replace(url[0], "")
                    self.companies_links.append(link)
                    # print(item["link"])
                i = i + 1

                # for item in data['icos']['data']:
                #     self.companies.append(DbCompany(**item))

                for key, value in data.items():
                    setattr(self, key, value)

                # COLLECTION.insert_many(data['icos']['data'])

        # return self.companies_links


    def get_data(self, url, i):
        param_page = f"page={i}"
        site_data = requests.get(url, params=param_page)
        return site_data.json()


class Ico:
    def __init__(self, ico_dict):
        for key, value in ico_dict.items():
            setattr(self, key, value)

if __name__ == '__main__':
    collection = ico_grab(api_url)
    print('***')



class IcoratingSpider(scrapy.Spider):
    name = 'icorating'
    allowed_domains = ['icorating.com']
    start_urls = ['https://icorating.com/ico/aid-coin/']

    ico_grab(start_urls)
    companies_links = ico_grab.companies_links


    def ico_page_parse(self, response):
        data = {'name': response.xpath('//h1[@class="c-heading c-heading--big"]/text()').get(),
                'Overview': response.xpath('//div[@class="mb15"]/text()').get(),
                'Features': response.xpath('//h2[@class="c-heading c-heading--big"]/text()').get(),
                'Investment_rating': response.xpath('//span[@class="c-card-info__name"]/text()').getall()[0],
                'Hype score ': response.xpath('//h1[@c-card-info__status fwn  na"]/text()').getall()[1],
                'Risk score ': response.xpath('//span[@class="c-card-info__status fwn"]/text()').getall()[2],
                },

        item = IcoParserItem(**data)

        yield item

    def parse(self, response):
        print("def_parse")

        for url in self.companies_links:
            yield response.follow(url=url, callback=self.ico_page_parse)

