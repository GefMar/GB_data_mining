from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import random

from pymongo import MongoClient

def a():
    time.sleep(1.0 + 2*random.random())

CLIENT = MongoClient('localhost', 27017)
MONGO_DB = CLIENT.hh_selenium
COLLECTION = MONGO_DB.resume

browser = webdriver.Firefox()

browser.get('http://hh.ru/')

a()
search_line = browser.find_element_by_css_selector('input.HH-Employer-ResumeSearch-Input')
search_line.send_keys('Программист')
a()
search_line.send_keys(Keys.RETURN)

a()
resumeSearch = browser.find_element_by_xpath('//*/div[contains(text(),"Резюме")]')
resumeSearch.click()
a()

def process_resume(resume_item):
    a()
    resume_item.click()
    a()
    browser.switch_to.window(browser.window_handles[1])

    try:
        resume = {
            'profile_url': browser.current_url.split('?')[0],
            'skills': [skill.text for skill in browser.find_elements_by_xpath('//div[@class="bloko-tag-list"]')],
            'work': browser.find_element_by_xpath('/html/body/div[6]/div/div/div[2]/div/div[2]/div/div/div/div[2]/div/div/div/div[2]/div[2]/div/div[1]/div/div[2]/div/div[1]/span').text
        }    

        _ = COLLECTION.insert_one(resume)
    except:
        pass

    browser.close()
    browser.switch_to.window(browser.window_handles[0])

while True:
    a()
    resume_items = browser.find_elements_by_class_name('resume-search-item__name')
    for resume_item in resume_items:
        process_resume(resume_item)

    try:
        browser.find_element_by_css_selector('a.HH-Pager-Controls-Next').click()
    except:
        break

browser.close()
