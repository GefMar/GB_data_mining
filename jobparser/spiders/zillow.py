# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import AvitoRealEstate
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class ZillowSpider(scrapy.Spider):
    name = 'zillow'
    allowed_domains = ['zillow.com', 'photos.zillowstatic.com', 'zillowstatic.com']
    start_urls = ['https://www.zillow.com/fort-worth-tx/']
    webdriver = webdriver.Firefox()

    def parse(self, response: HtmlResponse):
        real_estate_list = response.css(
            'div#grid-search-results ul.photo-cards li article a.list-card-link::attr(href)'
        )
        next = response.css('.zsg-pagination-next a::attr(href)').extract_first()
        yield response.follow(next, callback=self.parse)

        for adv in real_estate_list.extract():
            yield response.follow(adv, callback=self.pars_adv)

    def pars_adv(self, response: HtmlResponse):
        self.webdriver.get(response.url)
        media = self.webdriver.find_element_by_css_selector('.ds-media-col')
        photo_pic_img_len = len(self.webdriver.find_elements_by_xpath(
            '//ul[@class="media-stream"]/li/picture/source[@type="image/jpeg"]'))

        while True:
            media.send_keys(Keys.PAGE_DOWN)
            media.send_keys(Keys.PAGE_DOWN)
            media.send_keys(Keys.PAGE_DOWN)
            media.send_keys(Keys.PAGE_DOWN)
            tmp_len = len(self.webdriver.find_elements_by_xpath(
                '//ul[@class="media-stream"]/li/picture/source[@type="image/jpeg"]'))
            if photo_pic_img_len == tmp_len:
                break
            photo_pic_img_len = len(self.webdriver.find_elements_by_xpath(
                '//ul[@class="media-stream"]/li/picture/source[@type="image/jpeg"]'))

        images = [itm.get_attribute('srcset').split(' ')[-2] for itm in
                  self.webdriver.find_elements_by_xpath(
                      '//ul[@class="media-stream"]/li/picture/source[@type="image/jpeg"]')
                  ]

        yield AvitoRealEstate(title=self.webdriver.title, photos=images)
