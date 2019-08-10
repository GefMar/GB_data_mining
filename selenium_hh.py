from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from time import sleep
from pymongo import MongoClient


def parse_resume_list():
    resumes = browser.find_elements_by_css_selector('div.resume-search-item')
    for itm in resumes:
        itm.find_element_by_css_selector('a').click()
        browser.switch_to.window(browser.window_handles[1])
        resume = {
            'position': browser.find_element_by_css_selector('span.resume-block__title-text_position').text,
            'last_work': browser.find_element_by_css_selector('div.resume-block__sub-title').text,
            'link': browser.current_url}
        db['resumes'].insert_one(resume)
        browser.close()
        browser.switch_to.window(browser.window_handles[0])
        sleep(1)

mongo = MongoClient('', 27017)
db = mongo.hh
db.drop_collection('resumes')

browser = webdriver.Chrome(executable_path='C:\\Users\\...\\PycharmProjects\\GB_data_mining\\venv\\Scripts\\chromedriver.exe')
browser.get('https://perm.hh.ru/account/login?backurl=%2F')
login = browser.find_element_by_css_selector('input.bloko-input.HH-AuthForm-Login')
password = browser.find_element_by_css_selector('input.bloko-input.HH-AuthForm-Password')
login.send_keys('')
password.send_keys('')
password.send_keys(Keys.RETURN)

browser.get('https://hh.ru/search/resume?customDomain=1')
search_line = browser.find_element_by_css_selector('input.bloko-input.HH-Search-Wizard-Input')
search_line.send_keys('Hadoop')
search_line.send_keys(Keys.RETURN)

while True:
    parse_resume_list()
    try:
        next_link = browser.find_element_by_css_selector('a.bloko-button.HH-Pager-Controls-Next')
        next_link.click()
        sleep(1)
    except NoSuchElementException:
        break

print('Done')