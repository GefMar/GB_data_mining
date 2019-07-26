# -*- coding: utf-8 -*-
import scrapy
from ico_parser.items import IcoParserItem, PersonItem
from time import sleep


class IcobenchSpider(scrapy.Spider):
    name = 'icobench'
    allowed_domains = ['icobench.com']
    start_urls = ['https://icobench.com/icos?filterSort=name-asc']

    def ico_page_parse(self, response):
        # sleep(0.5)

        site_url = response.css('div.fixed_data div.financial_data a.button_big::attr(href)').get()
        social_urls = response.css('div.fixed_data div.socials a::attr(href)').getall()
        links = [site_url]
        links.extend(social_urls)

        ratings = []
        ratings_raw = response.css('#ratings div.rate')
        for rating_raw in ratings_raw:
            rating = rating_raw.css('div.col_3::text').getall()
            if len(rating) == 3:
                ratings.append({'Team': rating[0], 'Vision': rating[1], 'Product': rating[2]})
            else:
                # ICO analyzer bot - aggregate all rates
                pass

        people_raw = response.css('#team div.row')
        team = []
        # Found ICOs without team section
        if len(people_raw) > 0:
            team_raw = people_raw[0].css('div.col_3')
            for person_raw in team_raw:
                person_id = person_raw.css('a.image::attr(href)').get()
                person_name = response.css('#team div.row')[0].css('div.col_3')[0].css('a.image::attr(title)').get()
                person_job_title = response.css('#team div.row')[0].css('div.col_3')[0].css('h4::text').get()
                person_links = response.css('#team div.row')[0].css('div.col_3')[0].css('div.socials a::attr(href)').getall()
                person_data = {
                    'url_id': person_id,
                    'name': person_name,
                    'social_links': person_links
                }
                person_item = PersonItem(**person_data)
                team.append({'id':person_id, 'job_title':person_job_title})
                yield person_item

        advisers = []
        # Advisers exists
        if len(people_raw) > 1:
            advisers_raw = people_raw[1].css('div.col_3')
            for person_raw in advisers_raw:
                person_id = person_raw.css('a.image::attr(href)').get()
                person_name = response.css('#team div.row')[0].css('div.col_3')[0].css('a.image::attr(title)').get()
                person_job_title = response.css('#team div.row')[0].css('div.col_3')[0].css('h4::text').get()
                person_links = response.css('#team div.row')[0].css('div.col_3')[0].css('div.socials a::attr(href)').getall()
                person_data = {
                    'url_id': person_id,
                    'name': person_name,
                    'social_links': person_links
                }
                person_item = PersonItem(**person_data)
                advisers.append({'id':person_id, 'job_title':person_job_title})
                yield person_item

        data = {
            'name': response.css('div.ico_information div.name h1::text').get(),
            'slogan': response.css('div.ico_information div.name h2::text').get(),
            'description': response.css('div.ico_information p::text').get(),
            'tags': response.css('div.ico_information div.categories a::text').getall(),
            'links': links,
            'rating': ratings,
            'about': '\n'.join(response.css('#about p::text').getall()),
            'team': team,
            'advisers': advisers,
            'whitepaper_file_url': response.css('#whitepaper object::attr(data)')
        }

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
