# -*- coding: utf-8 -*-
import scrapy
import json
from w3lib.html import remove_tags
from ico_parser.items import IcoParserItem, PersonItem, IcoRatingItem


class IcoratingSpider(scrapy.Spider):
    name = 'icorating'
    allowed_domains = ['icorating.com']
    start_urls = ['https://icorating.com/ico/all/load/?page=1&sort=name&direction=asc']

    def ico_page_parse(self, response):

        name = response.xpath('//div[@id="ico-card"]/div[@class="o-grid o-grid--wrap"]'
                              '//div[@class="o-media__body o-media__body--center ml15"]/h1/text()').get().strip()

        headers = response.xpath('//div[@id="ico-card"]/div[@class="o-grid o-grid--wrap"]//h2/text()').getall()

        def get_description():
            text_overview = response.xpath('//div[@id="ico-card"]/div[@class="o-grid o-grid--wrap"]'
                                           '//div[@class="mb15"]').get()
            text_overview = remove_tags(text_overview).strip()

            if len(headers) == 3:
                text_features = ''
                features_all = response.xpath('//div[@id="ico-card"]/div[@class="o-grid o-grid--wrap"]'
                                              '//div[@class="mb25"]/p/text()').getall()

                for itm in features_all:
                    text_features = text_features + itm + ' '

                description = headers[0].strip() + ': ' + text_overview + ' ' + headers[1].strip() + ': ' + text_features
            else:
                description = headers[0].strip() + ': ' + text_overview

            return description.rstrip()


        rating_review_name = response.xpath('//div[@id="ico-card"]//h2[contains(text(), "Rating Review and Analytics")]'
                                            '/..//span[@class="c-card-info__name"]/text()').re(r'\w+.\w+')

        rating_review_val = response.xpath('.//div[@class="c-card-info__row mb10"]/span[2]/text()').re(r'\w+.')

        if len(rating_review_val) == 2:
            rating_review_val.insert(0, response.xpath('.//div[@class="c-card-info__row mb10"]'
                                                       '/span[3]/text()').getall()[0].strip())

        rating_review = dict(zip(rating_review_name, rating_review_val))


        data = {'name': name,
                'description': get_description(),
                'project_links': response.xpath('//*/div[contains(text(), "ICO Contacts")]/..//a/@href').getall(),
                'investment_rating': rating_review.get('Investment rating'),
                'hype_score': rating_review.get('Hype score'),
                'risk_score': rating_review.get('Risk score'),
                }

        item = IcoRatingItem(**data)

        yield item

    def parse(self, response):
        json_response = json.loads(response.text)

        current_page = json_response['icos']['current_page']
        if current_page < json_response['icos']['last_page']:
            next_page = f'https://icorating.com/ico/all/load/?page={current_page + 1}&sort=name&direction=asc'

            for page in json_response.get('icos').get('data'):
                yield response.follow(page.get('link'), callback=self.ico_page_parse)
                # print(page.get('link'))

            yield response.follow(next_page, callback=self.parse)

            print(current_page)
