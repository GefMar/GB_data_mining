# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse


class ZillowSpider(scrapy.Spider):
    name = 'zillow'
    allowed_domains = ['zillow.com']
    start_urls = ['https://www.zillow.com/fort-worth-tx/']

    def parse(self, response: HtmlResponse):
        real_estate_list = response.css(
            'div#grid-search-results ul.photo-cards li article a.list-card-link::attr(href)'
        )
        for link in real_estate_list:
            yield response.follow(link, callback=self.pars_adv)

    def pars_adv(self, response: HtmlResponse):
        pass
