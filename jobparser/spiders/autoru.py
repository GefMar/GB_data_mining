# -*- coding: utf-8 -*-
import scrapy


class AutoruSpider(scrapy.Spider):
    name = 'autoru'
    allowed_domains = ['auto.ru']
    start_urls = ['https://auto.ru/novorossiysk/cars/ford/all/']

    def parse(self, response):
        pass
