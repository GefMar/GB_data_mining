# -*- coding: utf-8 -*-
import scrapy
from ico_parser.items import IcoParserItem
from pymongo import MongoClient
from time import sleep
from ico_parser.items import PersonItem

CLIENT = MongoClient('localhost', 27017)
MONGO_DB = CLIENT.ico
COLLECTION = MONGO_DB.icobench


class IcobenchSpider(scrapy.Spider):
    name = 'icobench'
    allowed_domains = ['icobench.com']
    start_urls = ['https://icobench.com/icos?filterSort=name-asc']

    def ico_page_parse(self, response):
        sleep(0.1)

        data_persons = response.css('div#team.tab_content div.row')
        team = []
        advisors = []

        try:

            team = [
                {
                    'person': PersonItem(
                        source_page_url = item.css('a.image::attr(href)').get(),
                        name = item.css('h3::text').get(),
                        links = item.css('div.socials a::attr(href)').extract()),
                    'position': item.css('h4::text').get()}
                for item in data_persons[0].css('div.col_3')
            ]
        except IndexError as e:
            print(e)
            team = []

        try:
            advisors = [
                {
                    'person': PersonItem(
                        source_page_url=item.css('a.image::attr(href)').get(),
                        name=item.css('h3::text').get(),
                        links=item.css('div.socials a::attr(href)').extract()),
                    'position': item.css('h4::text').get()}
                for item in data_persons[1].css('div.col_3')
            ]
        except IndexError as e:
            print(e)
            advisors = []

        data = {'name': response.css('div.ico_information div.name h1::text').get(),
                'slogan': response.css('div.ico_information div.name h2::text').get(),
                'description': response.css('div.ico_information p::text').get(),
                'tags': response.css('div.ico_information div.categories a::text').extract(),
                # 'rating': response.css('div.fixed_data div.rating div.rate::text').get(),
                'rating': response.xpath('//div[@class ="rating"]/div[@itemprop="ratingValue"]/@content').getall(),
                'whitepaper_url': response.css('div.content div.tab_content a::attr(href)').get,
                'website': response.css('div.frame div.fixed_data div.financial_data a.button_big::attr(href)').get(),
                'preico_time': response.css('div.frame div.fixed_data div.financial_data div.number::text').get(),
                'type': response.css('div.frame div.fixed_data div.financial_data a::text').get(),
                'twiter_url': response.css('div#page div#profile_header div.frame div.fixed_data div.socials a.twitter::attr(href)').get(),
                'facebook_url': response.css('div#page div#profile_header div.frame div.fixed_data div.socials a.facebook::attr(href)').get(),
                'reddit_url': response.css('div#page div#profile_header div.frame div.fixed_data div.socials a.reddit::attr(href)').get(),
                'bitcointalk_url': response.css('div#page div#profile_header div.frame div.fixed_data div.socials a.bitcointalk::attr(href)').get(),
                'medium_url': response.css('div#page div#profile_header div.frame div.fixed_data div.socials a.medium::attr(href)').get(),
                'telegram_url': response.css('div#page div#profile_header div.frame div.fixed_data div.socials a.telegram::attr(href)').get(),
                'bitcoinwiki_url': response.css('div#page div#profile_header div.frame div.fixed_data div.socials a.bitcoinwiki::attr(href)').get(),
                'team': team,
                'advisors': advisors,
                }

        item = IcoParserItem(**data)

        # COLLECTION.insert_one(data)

        yield item

    def parse(self, response):
        next_page = response.css('div.ico_list div.pages a.next::attr(href)').get()
        ico_pages = response.css('div.ico_list td.ico_data div.content a.name::attr(href)').extract()

        for page in ico_pages:
            yield response.follow(page, callback=self.ico_page_parse)
            sleep(0.1)

        yield response.follow(next_page, callback=self.parse)

        print(next_page)
