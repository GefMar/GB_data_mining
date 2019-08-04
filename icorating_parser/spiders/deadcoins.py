# -*- coding: utf-8 -*-
import scrapy
from time import sleep


class DeadcoinsSpider(scrapy.Spider):
    name = 'deadcoind'
    allowed_domains = ['deadcoins.com']
    start_urls = ['https://deadcoins.com/?pagenum=1']
    current_page = 1
    last_page = 0

    def ico_page_parse(self, response):
        coin_name = response.xpath('//tr[@id="gv-field-1-13"]/td/text()').get()
        coin_code = response.xpath('//tr[@id="gv-field-1-3"]/td/text()').get()
        coin_descr = response.xpath('//tr[@id="gv-field-1-14"]/td/p/text()').get()
        coin_link = response.xpath('//tr[@id="gv-field-1-18"]/td/a/@href').get()
        coin_cat = response.xpath('//tr[@id="gv-field-1-16"]/td/text()').get()
        coin_entry_date = response.xpath('//tr[@id="gv-field-1-date_created"]/td/text()').get()
        print("+++++++ Coin done: {}".format(response.url))

    def parse(self, response):

        if self.current_page == 10:
            print('==================== Current page: {}. Exit!'.format(self.current_page))
            return
        else:
            print('==================== Current page: {}. Let\'s  parse something!'.format(self.current_page))
            links = response.xpath('//*[@id="gv-item-reviewed"]').re('https://deadcoins.com/entry/\d{4}/\?gvid')
            print('There are {} links on page {}.'.format(len(links), self.current_page))
            if not self.last_page:
                self.last_page = response.xpath('//span[@class="page-numbers dots"]/../following-sibling::*/a/text()').get()

        for item in links:
            sleep(0.5)
            print("Going to: {}".format(item))
            yield response.follow(item, callback=self.ico_page_parse)

        self.current_page += 1
        next_page = 'https://deadcoins.com/?pagenum={}'.format(self.current_page)
        yield response.follow(next_page, callback=self.parse)