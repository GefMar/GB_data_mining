import scrapy
from scrapy.selector import Selector
from ico_parser.items import IcoRatingItem
import datetime
import json
import re


class IcoRatingSpider(scrapy.Spider):
    name = 'icoraring'
    allowed_domains = ['icorating.com']

    current_page = 1
    start_urls = ['https://icorating.com/ico/all/load/?sort=investment_rating&direction=desc&page=%s' % current_page]

    def ico_page_parse(self, response):
        selector = Selector(response)

        def get_person(person):
            return {
                'profile': person.xpath('descendant::td[1]/div/div[1]/a/@href').get(),
                'name': person.xpath('descendant::td[1]/div/div[1]/a/@title').get(),
                'position': re.sub("^\s+|\s+$", "", person.xpath('descendant::td[2]/text()').get(), flags=re.UNICODE),
                'social': person.xpath('descendant::td[4]//a/@href').get()
            }

        data = {
            'name': re.sub("^\s+|\s+$", "", selector.css('.o-media .c-heading--big::text').get(), flags=re.UNICODE),
            'description': {
                'overview': selector.css('.mb15 p::text').get(),
                'features': selector.css('.mb25 p::text').get()
            },
            'socials': selector.css('.c-card-info .c-social-icons a::attr("href")').getall(),
            'ratings': {
                re.sub("^\s+|\s+$", "", row.css('.c-card-info__name::text').get(), flags=re.UNICODE):
                re.sub("^\s+|\s+$", "", row.xpath('(descendant::span)[last()]/text()').get(), flags=re.UNICODE)
                for row in selector.css('.c-card-info--va-top .c-card-info__row')
            },
            'team': {
                'team': [get_person(person)
                         for person in selector.xpath('(//div[@id="team"]//table[@class="c-table"])[1]/tbody/tr')],
                'advisors': [get_person(person)
                             for person in selector.xpath('(//div[@id="team"]//table[@class="c-table"])[2]/tbody/tr')]
            },
            'iso_times': {
                'Start ICO': re.sub("^\s+|\s+$", "",
               selector.xpath('//table[@class="c-card-info__table"]//tr[contains(th/text(), "Start ICO")]/td/text()').get(''), flags=re.UNICODE),
                'End ICO': re.sub("^\s+|\s+$", "",
               selector.xpath('//table[@class="c-card-info__table"]//tr[contains(th/text(), "End ICO")]/td/text()').get(''), flags=re.UNICODE),
            }
        }

        for key, value in data['iso_times'].items():
            if value:
                data['iso_times'][key] = datetime.datetime.strptime(value, '%d %b %Y')

        yield IcoRatingItem(**data)

    def parse(self, response):
        # if current page not start with 1 need same request
        yield response.follow(self.start_urls[0], callback=self.parse_from_page)

    def parse_from_page(self, response):
        raw_json = json.loads(response.body_as_unicode())
        json_icos = raw_json.get('icos')

        if json_icos.get('current_page') > json_icos.get('last_page'):
            print(f"parsing done. last page is {self.current_page - 1}")
            return

        self.current_page += 1
        next_page = '='.join([self.start_urls[0].rsplit('=', 1)[0], str(self.current_page)])

        for item in json_icos.get('data'):
            yield response.follow(item.get('link'), callback=self.ico_page_parse)
            print(item.get('link'))

        yield response.follow(next_page, callback=self.parse_from_page)
