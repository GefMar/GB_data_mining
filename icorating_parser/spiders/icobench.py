# -*- coding: utf-8 -*-
import scrapy
from icorating_parser.items import IcobenchParserItem
from w3lib.html import remove_tags
from scrapy.selector import Selector

class IcobenchSpider(scrapy.Spider):
    name = 'icobench'
    allowed_domains = ['icobench.com']
    start_urls = ['https://icobench.com/icos?filterSort=name-asc']

    def ico_page_parse(self, response):

        # get team
        team = []
        team_count = len(response.css('#team div.col_3').getall())
        for i in range(0, team_count):
            member = response.css('#team div.row div.col_3').getall()[i]
            name = Selector(text=member).css('h3::text').get()
            name = name.replace('.', '_')
            team.append({
                'name': name,
                'position': Selector(text=member).css('h4::text').get(),
                'socials': Selector(text=member).css('div.socials a::attr(href)').get()
            })

        # get financial data
        financial_data = {}
        params_count = len(response.xpath('//div[@class="financial_data"]//div[@class="data_row"]').getall())
        for i in range(1, params_count+1):
            param = remove_tags(response.xpath('//div[@class="financial_data"]//div[@class="data_row"][{}]/div[contains(@class, "col_2")]'.format(i)).getall()[0]).strip()
            value = remove_tags(response.xpath('//div[@class="financial_data"]//div[@class="data_row"][{}]/div[contains(@class, "col_2")]'.format(i)).getall()[1]).strip()
            financial_data[param] = value

        pre_ico_time = response.xpath(
            '//div[@class="financial_data"]//div[@class="col_2 expand"]/label[starts-with(text(), "PreICO time")]/following-sibling::small/text()').get()
        ico_time = response.xpath(
            '//div[@class="financial_data"]//div[@class="col_2 expand"]/label[starts-with(text(), "ICO Time")]/following-sibling::small/text()').get()

        data = {
            'name': response.css('div.ico_information div.name h1::text').get(),
            'slogan': response.css('div.ico_information div.name h2::text').get(),
            'description': response.css('div.ico_information p::text').get(),
            'tags': response.css('div.ico_information div.categories a::text').getall(),
            'website': response.css('div.financial_data a.button_big::attr(href)').get(),
            'socials': response.css('div.fixed_data div.socials a::attr(href)').getall(),
            'ratings': {
                'overall': response.css('div.rating div[itemprop="ratingValue"]::attr(content)').get(),
                'profile': response.css('div.distribution div.col_4 div::text').getall()[1].strip(),
                'team': response.css('div.distribution div.col_75 div.columns div::text').getall()[0].strip(),
                'vision': response.css('div.distribution div.col_75 div.columns div::text').getall()[2].strip(),
                'product': response.css('div.distribution div.col_75 div.columns div::text').getall()[4].strip()
            },
            'about': remove_tags(' '.join(response.css('div#profile_content div.content div#about p').getall())),
            'team': team,
            'whitepaper': response.css('div#profile_content div#whitepaper object::attr(data)').get(),
            'financial_data': financial_data,
            'url_on_icobench': response.url,
            'pre_ico_time': pre_ico_time,
            'ico_time': ico_time
        }

        item = IcobenchParserItem(**data)
        yield item

    def parse(self, response):

        next_page = response.css('div.ico_list div.pages a.next::attr(href)').get()
        ico_pages = response.css('div.ico_list td.ico_data div.content a.name::attr(href)').extract()

        for page in ico_pages:
            yield response.follow(page.lower(), callback=self.ico_page_parse)

        yield response.follow(next_page, callback=self.parse)

        print(next_page)