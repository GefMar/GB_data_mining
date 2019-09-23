# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem


class SuperjobSpider(scrapy.Spider):
    name = 'superjob'
    allowed_domains = ['superjob.ru']
    start_urls = ['https://www.superjob.ru/vacancy/search/?keywords=python&geo%5Bc%5D%5B0%5D=1']

    def parse(self, response: HtmlResponse):
        vacancy_urls = response.xpath('//a[contains(@class, "icMQ_") and contains(@class, "_1QIBo")]/@href').extract()
        next_page = response.xpath('//div[contains(@class, "L1p51")]/a[@rel="next"]/@href').extract_first()
        yield response.follow(next_page, callback=self.parse)
        for vac in vacancy_urls:
            yield response.follow(vac, callback=self.parse_vacancy)

    def parse_vacancy(self, response: HtmlResponse):
        _tmp_cur = {'₽': 'RUB', '$': 'USD'}
        name = response.xpath("//div[@class='_3MVeX']/h1/text()").extract_first()
        _tmp_values = response.xpath("//div[@class='_3MVeX']/span[contains(@class, '_3mfro')]/span/text()").extract()
        v_tmp = [int(itm.replace('\xa0', '')) for itm in _tmp_values[:-1] if itm.replace('\xa0', '').isdigit()]
        salary = {'currency': (lambda x: _tmp_cur[x] if x and x in _tmp_cur else None)(
            _tmp_values[-1]) if _tmp_values else None,
                  'min_value': v_tmp[0] if v_tmp else None,
                  'max_value': v_tmp[1] if v_tmp and len(v_tmp) > 1 else None,
                  }

        yield JobparserItem(name=name, salary=salary)
