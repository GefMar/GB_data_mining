# -*- coding: utf-8 -*-
import scrapy
import time
import random
from hh_parser.items import HhParserItem
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class HhRuSpider(scrapy.Spider):
    name = 'hh.ru'
    allowed_domains = ['hh.ru']

    def page_parse(self, response):
        browser = webdriver.Chrome()
        link = 'https://hh.ru' + response.meta.get('resume_link')
        browser.get(link)
        time.sleep(1)
        last_company = browser.find_element_by_xpath('//div[@class="resume-block__sub-title"]/span').text
        get_skills = browser.find_elements_by_xpath('//div[@class="bloko-tag-list"]//span[@data-qa="bloko-tag__text"]/span')
        skills = []
        for itm in get_skills:
            skills.append(itm.text)
        data = {
            'last_company': last_company,
            'skills': skills,
            'resume_link': link,
        }
        browser.close()

        item = HhParserItem(**data)

        yield item

    start_urls = ['https://hh.ru/search/resume?area=1&clusters=true&exp_period=all_time&logic=normal&pos=full_text&from=employer_index_header&text=Программист']

    def parse(self, response):
        next_page = response.css('a.HH-Pager-Controls-Next::attr(href)').get()
        resume_pages = response.xpath('//div[@class="resume-search-item__content-layout"]//a[@itemprop="jobTitle"]/@href').getall()

        for page in resume_pages:
            time.sleep(0.5)
            yield response.follow(page, callback=self.page_parse, meta={'resume_link': page})

        time.sleep(1)
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
            print(next_page)
