from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

from pymongo import MongoClient

CLIENT = MongoClient('localhost', 27017)
CLIENT.drop_database('HH_resume')
MONGO_DB = CLIENT.HH_resume
COLLECTION = MONGO_DB.resume_coll

url = 'https://hh.ru/employer'
sleep = 3
next_link = True
browser = webdriver.Chrome()

browser.get(url)
search_line = browser.find_element_by_css_selector('input.HH-Supernova-Search-Input')
time.sleep(sleep)
search_line.send_keys('Арматурщик')
# Арматурщик - механик в автосервисе, который разбирает и собирает автомобили, для кузовного ремонта.
time.sleep(sleep)
search_line.send_keys(Keys.RETURN)
time.sleep(sleep)
# закрытие окна подтверждения региона
browser.find_element_by_xpath('.//div[@class="navi-region-clarification-wrapper"]/button[@type="button"]').send_keys(Keys.ENTER)


def page_resume(i):  # функция обхода и выбора данных страницы резюме
    resumes = browser.find_elements_by_css_selector('div.resume-search-item__content')
    time.sleep(sleep)
    link = browser.find_element_by_xpath('.//a[@itemprop="jobTitle"]').get_attribute('href')
    resumes[i].find_element_by_css_selector('a').click()
    browser.switch_to.window(browser.window_handles[1])
    time.sleep(sleep)
    try:
        gender = browser.find_element_by_xpath('//span[@itemprop="gender"]').text
    except:
        gender = None
    try:
        age = browser.find_element_by_xpath('//span[@data-qa="resume-personal-age"]').text
    except:
        age = None
    try:
        last_work = browser.find_element_by_xpath('//div[@itemprop = "name"]').text
    except:
        last_work = None
    try:
        tags = browser.find_element_by_xpath('//div[@class="bloko-tag-list"]').text
    except:
        tags = None
    data = {'gender': gender,
            'age': age,
            'last_work': last_work,
            'tags': tags,
            'link': link
            }
    browser.close()
    time.sleep(2)
    browser.switch_to.window(browser.window_handles[0])
    resume_coll.append(data)

    return


while next_link:  # обход пагинатора
    resume_coll = []
    try:
        for i in range(20):  # обход страницы поиска
            page_resume(i)
    except:
        COLLECTION.insert_many(resume_coll)
        print('-'*10)

    try:
        next_link = browser.find_element_by_css_selector('a.HH-Pager-Controls-Next')
    except:
        print('-'*20)
        break
    COLLECTION.insert_many(resume_coll)
    next_link.click()

browser.close()
