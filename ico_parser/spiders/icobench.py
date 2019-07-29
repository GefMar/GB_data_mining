# -*- coding: utf-8 -*-
import scrapy
from ico_parser.items import IcoParserItem, PersonItem, RatingItem  # , IcoParserPeople
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
        data_persons = response.css('div#team.tab_content div.row')

        try:
            team = [
                {
                    'person': PersonItem(
                        source_page_url=item.css('a.image::attr(href)').get(),
                        name=item.css('h3::text').get(),
                        links=item.css('div.socials a::attr(href)').extract()),
                    'position': item.css('h4::text').get()
                }
                for item in data_persons[0].css('div.col_3')
            ]
        except IndexError as e:
            # print(e)
            team = []

        try:
            advisors = [
                {
                    'person': PersonItem(
                        source_page_url=item.css('a.image::attr(href)').get(),
                        name=item.css('h3::text').get(),
                        links=item.css('div.socials a::attr(href)').extract()),
                    'position': item.css('h4::text').get()
                }
                for item in data_persons[1].css('div.col_3')
            ]
        except IndexError as e:
            # print(e)
            advisors = []

        try:
            overall_rating = response.css('div.fixed_data div.rating div::attr(content)').get()
        except IndexError as e:
            overall_rating = []
        try:
            profile_rating = response.css('div.fixed_data div.rating div.distribution div.col_4 div.wrapper').re(
                '\d.\d')
        except IndexError as e:
            profile_rating = []
        try:
            team_rating = \
                response.css('div.fixed_data div.rating div.distribution div.col_75 div.wrapper div.columns').re(
                    '\d.\d')[0]
        except IndexError as e:
            team_rating = []
        try:
            vision_rating = \
                response.css('div.fixed_data div.rating div.distribution div.col_75 div.wrapper div.columns').re(
                    '\d.\d')[1]
        except IndexError as e:
            vision_rating = []
        try:
            product_rating = \
                response.css('div.fixed_data div.rating div.distribution div.col_75 div.wrapper div.columns').re(
                    '\d.\d')[2]
        except IndexError as e:
            product_rating = []

        rating = [{
            'overall_rating': overall_rating,
            'profile_rating': profile_rating,
            'team_rating': team_rating,
            'vision_rating': vision_rating,
            'product_rating': product_rating,
        }]

        data = {'name': response.css('div.ico_information div.name h1::text').get(),
                'slogan': response.css('div.ico_information div.name h2::text').get(),
                'description': response.css('div.ico_information p::text').get(),
                'tag': response.css('div.ico_information div.categories a::text').getall(),
                'rating': rating,
                'project_url': response.css('div.fixed_data a.button_big::attr(href)').get(),
                'about_project': response.css('div.frame div#about.tab_content p::text').getall(),
                'team': team,
                'advisors': advisors,
                'pre_ico_time_begin': response.css('div.fixed_data div.row small::text').re('\d\d\d\d-\d\d-\d\d')[0],
                'pre_ico_time_end': response.css('div.fixed_data div.row small::text').re('\d\d\d\d-\d\d-\d\d')[1],
                }

        item = IcoParserItem(**data)
        # people = IcoParserPeople(**data)

        yield item  # , people

    def parse(self, response):

        next_page = response.css('div.ico_list div.pages a.next::attr(href)').get()
        ico_pages = response.css('div.ico_list td.ico_data div.content a.name::attr(href)').extract()

        for page in ico_pages:
            yield response.follow(page, callback=self.ico_page_parse)
            # sleep(1)

        yield response.follow(next_page, callback=self.parse)

        print(next_page)
