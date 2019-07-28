# -*- coding: utf-8 -*-
import scrapy
from ico_parser.items import IcoParserItem, PersonItem


class IcobenchSpider(scrapy.Spider):
    name = 'icobench'
    allowed_domains = ['icobench.com']
    start_urls = ['https://icobench.com/icos?filterSort=name-asc']

    def ico_page_parse(self, response):

        def socials_parse():
            names = response.css('div.socials a::text').extract()
            links = response.css('div.socials a::attr(href)').extract()
            return dict(zip(names, links))

        # def rating_parse():
        #     ratings = {'profile': None,
        #                'team': None,
        #                'vision': None,
        #                'product': None
        #                }
        #     experts_rating = response.css('div.fixed_data div.col_75 div.columns div.col_4::text').extract()
        #     ratings['team_rating'] = experts_rating[0].replace('-', 'None').strip()
        #     ratings['vision_rating'] = experts_rating[2].replace('-', 'None').strip()
        #     ratings['product_rating'] = experts_rating[4].replace('-', 'None').strip()
        #     return ratings

        def about_parse():
            about_string = ''
            about_all = response.css('div#profile_content div#about p::text').extract()
            for about in about_all:
                about_string = about_string + about + ' '
            return about_string.rstrip()

        data_persons = response.css('div.tab_content#team div.row')

        try:

            team = [
                {
                    'person': PersonItem(
                        person_url=itm.css('a::attr(href)').get(),
                        name=itm.css('h3::text').get(),
                        social_links=itm.css('div.socials a::attr(href)').extract()),
                    'position': itm.css('h4::text').get()
                }
                for itm in data_persons[0].css('div.col_3')
            ]


        except IndexError as error:
            #print(error)
            team = []

        try:
            advisors = [
                {
                    'person': PersonItem(
                        person_url=itm.css('a::attr(href)').get(),
                        name=itm.css('h3::text').get(),
                        social_links=itm.css('div.socials a::attr(href)').extract()),
                    'position': itm.css('h4::text').get()
                }
                for itm in data_persons[1].css('div.col_3')
            ]

            try:
                for itm in data_persons[2].css('div.col_3'):
                    tmp_person = {
                        'person': PersonItem(
                            person_url=itm.css('a::attr(href)').get(),
                            name=itm.css('h3::text').get(),
                            social_links=itm.css('div.socials a::attr(href)').extract()),
                        'position': itm.css('h4::text').get()
                    }
                    advisors.append(tmp_person)

            except:
                pass

        except IndexError as error:
            #print(error)
            advisors = []

        data = {'name': response.css('div.ico_information div.name h1::text').get(),
                'slogan': response.css('div.ico_information div.name h2::text').get(),
                'description': response.css('div.ico_information p::text').get(),
                'categories': response.css('div.categories a::text').extract(),
                'official_link': response.css('div.financial_data a.button_big::attr(href)').get(),
                'project_social_links': socials_parse(),
                # 'ratings': rating_parse(),
                'experts_ratings': rating_parse(),
                'about': about_parse(),
                'team': team,
                'advisors': advisors
                }

        item = IcoParserItem(**data)

        yield item

    def parse(self, response):
        next_page = response.css('div.ico_list div.pages a.next::attr(href)').get()
        ico_pages = response.css('div.ico_list td.ico_data div.content a.name::attr(href)').extract()

        for page in ico_pages:
            yield response.follow(page, callback=self.ico_page_parse)

        yield response.follow(next_page, callback=self.parse)

        print(next_page)
