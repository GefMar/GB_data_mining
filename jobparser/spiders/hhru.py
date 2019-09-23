# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem


class HhruSpider(scrapy.Spider):
    name = 'hhru'
    allowed_domains = ['hh.ru']
    start_urls = ['https://hh.ru/search/vacancy?text=Python&area=113&st=searchVacancy']

    def parse(self, response: HtmlResponse):
        next_page = response.css('a.HH-Pager-Controls-Next::attr(href)').extract_first()
        yield response.follow(next_page, callback=self.parse)

        vacancy = response.css(
            'div.vacancy-serp div.vacancy-serp-item div.vacancy-serp-item__row_header a.bloko-link::attr(href)').extract()

        for link in vacancy:
            yield response.follow(link, callback=self.vacansy_parse)

    def vacansy_parse(self, response: HtmlResponse):
        name = response.css('div.vacancy-title h1.header::text').extract_first()

        salary = {'currency': response.xpath(
            '//span[@itemprop="baseSalary"]//meta[contains(@itemprop, "currency")]/@content').extract_first(),
                  'min_value': response.xpath(
                      '//span[@itemprop="baseSalary"]/span[@itemprop="value"]/meta[@itemprop="minValue"]/@content').extract_first(),
                  'max_value': response.xpath(
                      '//span[@itemprop="baseSalary"]/span[@itemprop="value"]/meta[@itemprop="maxValue"]/@content').extract_first()}

        yield JobparserItem(name=name, salary=salary)
