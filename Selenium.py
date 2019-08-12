from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from login_data import hh_login, hh_pwd
from time import sleep
from w3lib.html import remove_tags
from pymongo import MongoClient
from random import random

CLIENT = MongoClient('localhost', 27017)
MONGO_DB = CLIENT.hh_ru
COLLECTION = MONGO_DB.resumes

browser = webdriver.Firefox()
browser.get('https://hh.ru/')
job_title = 'Программист Python Data Science'
wait = WebDriverWait(browser, 20)

sleep(2)
browser.find_element_by_css_selector('span.bloko-icon_cancel').click()

login_form = browser.find_element_by_css_selector('input.HH-AuthForm-Login')
wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'input.HH-AuthForm-Login'))).click()
# login_form.click()
login_form.send_keys(hh_login)
pwd_form = browser.find_element_by_css_selector('input.HH-AuthForm-Password')
login_form.click()
pwd_form.send_keys(hh_pwd)
pwd_form.send_keys(Keys.ENTER)

sleep(1)

search_form = browser.find_element_by_css_selector('input.HH-Supernova-Search-Input')
search_form.send_keys(job_title)
search_form.send_keys(Keys.ENTER)

sleep(1)

wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@data-hh-tab-id="resumeSearch"]')))
resume_tab = browser.find_element_by_xpath('//div[@data-hh-tab-id="resumeSearch"]')

resume_tab.click()

sleep(1)


def process_resumes():
    sleep(2)
    window_after = browser.window_handles[1]
    browser.switch_to.window(window_after)
    try:
        title = [itm.text for itm in browser.find_elements_by_css_selector('span.resume-block__title-text')]
    except NoSuchElementException as e:
        print(e)
        title = []
    try:
        skills = [skill.text for skill in browser.find_elements_by_xpath('//div[@class="bloko-tag-list"]')]
    except NoSuchElementException as e:
        print(e)
        skills = []
    try:
        last_work = browser.find_element_by_css_selector(
            'div[data-qa="resume-block-experience"] div.bloko-columns-row > div.resume-block-item-gap').text
    except NoSuchElementException as e:
        print(e)
        last_work = []
    try:
        my_url = browser.current_url.split('?')[0]
    except NoSuchElementException as e:
        print(e)
        my_url = []

    resume = {
        'title': title,
        'last_work_place': last_work,
        'skills': skills,
        'url': my_url
    }

    _ = COLLECTION.insert_one(resume)

    browser.close()
    browser.switch_to.window(browser.window_handles[0])


page = 1

while True:
    resumes_list = browser.find_elements_by_css_selector('a.resume-search-item__name')
    for item in resumes_list:
        item.click()
        process_resumes()
        sleep(random() * 3)
    try:
        browser.find_element_by_css_selector('a.HH-Pager-Controls-Next').click()
        sleep(random() * 3)
    except NoSuchElementException:
        break
    page += 1

browser.close()
