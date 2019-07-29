# -*- coding: utf-8 -*-
import scrapy
from ico_parser.items import IcoParserItem #, IcoParserPeople
from pymongo import MongoClient
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
        data = {'name': response.css('div.ico_information div.name h1::text').get(),
                'slogan': response.css('div.ico_information div.name h2::text').get(),
                'description': response.css('div.ico_information p::text').get(),
                'tag': response.css('div.ico_information div.categories a::text').getall(),
                'rating': response.css('div.fixed_data div.rating div::attr(content)').get(),
                'project_url': response.css('div.fixed_data a.button_big::attr(href)').get(),
                'about_project': response.css('div.frame div#about.tab_content p::text').getall(),
                'team_names': response.css('div.frame div#team.tab_content div.row h3::text').getall(),
                'team_title': response.css('div.frame div#team.tab_content div.row h4::text').getall(),
                'team_linkedin': response.css('div.frame div#team.tab_content div.row div.socials a::attr(href)').getall(),
                }

        item = IcoParserItem(**data)
        # people = IcoParserPeople(**data)

        yield item #, people

    def parse(self, response):

        next_page = response.css('div.ico_list div.pages a.next::attr(href)').get()
        ico_pages = response.css('div.ico_list td.ico_data div.content a.name::attr(href)').extract()

        for page in ico_pages:
            yield response.follow(page, callback=self.ico_page_parse)
            # sleep(1)

        yield response.follow(next_page, callback=self.parse)

        print(next_page)
