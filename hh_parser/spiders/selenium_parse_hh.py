# -*- coding: utf-8 -*-
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import scrapy
from pymongo import MongoClient

from hh_parser.Items import hhParserItem

CLIENT = MongoClient('localhost', 27017)
MONGO_DB = CLIENT.ico
COLLECTION = MONGO_DB.hh


# class hhSpider(scrapy.Spider):
class hhSpider():
    resume_urls = []
    browser = webdriver.Firefox()
    browser.get("https://tyumen.hh.ru/employer")
    time.sleep(1)
    search_line = browser.find_element_by_xpath("//div[@class='bloko-input-wrapper']/input[1]")
    search_line.clear()
    search_line.send_keys("Python")
    search_line.send_keys(Keys.RETURN)
    time.sleep(1)

    # def parse(self, response):
    def parse(self, url):
        self.browser.execute_script(f"window.open('{url}', 'hh_resume_page')")
        self.browser.switch_to.window(self.browser.window_handles[1])
        print(self.browser.title)
        time.sleep(1)

        # skills = browser.find_elements_by_xpath("//div[@class='bloko-tag-list']")[0].text.split("\n")
        # workplace = browser.find_elements_by_xpath("//div[@class='resume-block-container']/div[@itemprop='name']")[0].text

        data = {'url': url,
                'skills': self.browser.find_elements_by_xpath("//div[@class='bloko-tag-list']")[0].text.split(
                    "\n").get(),
                'workplace':
                    self.browser.find_elements_by_xpath("//div[@class='resume-block-container']/div[@itemprop='name']")[
                        0].text.get(),
                },
        self.browser.close()
        item = hhParserItem(**data)
        yield item

    # def resumes_page_parse(self, response):
    def resumes_page_parse(self):
        # next_page = self.browser.find_elements_by_xpath("//a[@data-qa='pager-next']").get_attribute("href")
        resume_as = self.browser.find_elements_by_xpath("//div[@class='resume-search-item__header']/a")
        for resume_a in resume_as:
            self.resume_urls.append(resume_a.get_attribute("href"))

        for url in self.resume_urls:
            # yield response.follow(url, callback=self.resumes_page_parse)
            self.parse(self, url)
            # sleep(1)

        # yield response.follow(next_page, callback=self.parse)
        # print(next_page)


HHSpider = hhSpider()
HHSpider.resumes_page_parse()
