# -*- coding: utf-8 -*-
import scrapy
from ico_parser.items import IcoParserItem, PersonItem
from pymongo import MongoClient
import re
from time import sleep


CLIENT = MongoClient('localhost', 27017)
MONGO_DB = CLIENT.ico
COLLECTION = MONGO_DB.icobench


class IcobenchSpider(scrapy.Spider):
    name = 'icobench'
    allowed_domains = ['icobench.com']
    start_urls = ['https://icobench.com/icos?filterSort=name-asc']

    def ico_page_parse(self, response):
        # sleep(0.5)

        data_persons = response.css('div#team.tab_content div.row')
        # team_tmp = []
        # for person_item in data_persons[0].css('div.col_3'):
        #     person_tmp = PersonItem(
        #         source_page_url = person_item.css('div.a::attr(href)').get(),
        #         name = person_item.css('h3::text()').get(),
        #         links = person_item.css('div.socials div.a::attr(href)').extract()
        #     )
        #     final_strict = {'person':person_tmp,'position':person_item.css('h4::text()').get()}
        #     # team_tmp.append(person_tmp)
        #     team_tmp.append(final_strict)

        try:
            team = [
                {
                    'person': PersonItem(
                        source_page_url=person_item.css('a.image::attr(href)').get(),
                        name=person_item.css('h3::text').get(),
                        links=person_item.css('div.socials a::attr(href)').extract()),
                    'position': person_item.css('h4::text').get()}
                for person_item in data_persons[0].css('div.col_3')
            ]
        except IndexError as e:
            print(e)
            team = []

        try:
            advisors = [
                {
                    'person': PersonItem(
                        source_page_url=person_item.css('div.a::attr(href)').get(),
                        name=person_item.css('h3::text').get(),
                        links=person_item.css('div.socials div.a::attr(href)').extract()),
                    'position': person_item.css('h4::text').get()}
                for person_item in data_persons[1].css('div.col_3')
            ]
        except IndexError as e:
            print(e)
            advisors = []

        data = {'name': response.css('div.ico_information div.name h1::text').get(),
                'slogan': response.css('div.ico_information div.name h2::text').get(),
                'description': response.css('div.ico_information p::text').get(),
                'categories': response.css('div.ico_information div.categories a::text').getall(),
                'socials': response.css('div.fixed_data div.socials a::attr(href)').getall(),
                'rating':
                    {'profile': response.css('div.fixed_data div.wrapper').xpath('//span[text()="Benchy"]/../text()').re(r'(\d+.\d+)')[0],
                     'team': response.css('div.fixed_data div.wrapper').xpath('//div[@class="col_4 col_3"][1]').re(r'(\d+.\d+)')[0],
                     'vision': response.css('div.fixed_data div.wrapper').xpath('//div[@class="col_4 col_3"][2]').re(r'(\d+.\d+)')[0],
                     'product': response.css('div.fixed_data div.wrapper').xpath('//div[@class="col_4 col_3"][3]').re(r'(\d+.\d+)')[0],
                     },
                'about': response.xpath('//div[@id="about"]/p/text()').getall(),
                'team': team,
                'advisors': advisors,
                'time_preico': response.xpath('//div[@class="col_2 expand"]//small[1]/text()').getall()[0],
                'time_ico': response.xpath('//div[@class="col_2 expand"]//small[1]/text()').getall()[1],

                'finance':
                    {'token': response.xpath('//div[@class="financial_data"]//div[@class="data_row"][1]//div[@class="col_2"][2]//b/text()').get(),
                    'type': response.xpath('//div[@class="financial_data"]//div[@class="data_row"][2]//div[@class="col_2"][2]//a/text()').get(),
                    'price_preico': response.xpath('//div[@class="financial_data"]//div[@class="data_row"][3]//div[@class="col_2"][2]//b/text()').get(),
                    'price': response.xpath('//div[@class="financial_data"]//div[@class="data_row"][4]//div[@class="col_2"][2]//b/text()').get(),
                    'bonus': response.xpath('//div[@class="financial_data"]//div[@class="data_row"][5]//div[@class="col_2"][2]//b/text()').get(),
                    'bounty': response.xpath('//div[@class="financial_data"]//div[@class="data_row"][6]//div[@class="col_2"][2]//b/text()').get(),
                    'mvp_prototype': response.xpath('//div[@class="financial_data"]//div[@class="data_row"][7]//div[@class="col_2"][2]//b/text()').get(),
                     }

                },

        item = IcoParserItem(**data)

        yield item

    def parse(self, response):

        next_page = response.css('div.ico_list div.pages a.next::attr(href)').get()
        ico_pages = response.css('div.ico_list td.ico_data div.content a.name::attr(href)').extract()

        for page in ico_pages:
            yield response.follow(page, callback=self.ico_page_parse)
            # sleep(1)

        yield response.follow(next_page, callback=self.parse)

        print(next_page)
