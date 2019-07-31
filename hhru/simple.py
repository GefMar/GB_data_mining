from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from time import sleep
from pymongo import MongoClient

print(f'parsing start')

query = 'Программист'

CLIENT = MongoClient('192.168.0.202', 27017)
COLLECTION = CLIENT.hhru.resume

binary = FirefoxBinary(r"C:\Program Files\Mozilla Firefox\firefox.exe")
browser = webdriver.Firefox(firefox_binary=binary, executable_path=r'.\bin\geckodriver.exe')
browser.get('https://hh.ru/?customDomain=1')

# search
try:
    browser.find_element_by_css_selector('a[data-qa="mainmenu_employer"]').click()
except NoSuchElementException:
    browser.find_element_by_css_selector('a[data-qa="mainmenu_searchresumes"]').click()

sleep(1)

search = browser.find_element_by_css_selector('.HH-Employer-ResumeSearch-Input')
search.send_keys(query)
search.send_keys(Keys.RETURN)

sleep(2)


def process_result_item(item):
    item.find_element_by_css_selector('.resume-search-item__name').click()
    sleep(1)
    browser.switch_to.window(browser.window_handles[1])

    resume = {
        'profile_url': browser.current_url.split('?')[0],
        'skills': [skill.text for skill in browser.find_elements_by_css_selector(
            '[data-qa="skills-table"] .bloko-tag-list .bloko-tag span')],
        'work': browser.find_element_by_css_selector(
            'div[data-qa="resume-block-experience"] div.bloko-columns-row > div.resume-block-item-gap').text
    }

    _ = COLLECTION.insert_one(resume)
    print(f'\tresume saved _id="{_.inserted_id}"')

    browser.close()
    browser.switch_to.window(browser.window_handles[0])


page = 1
while True:
    items = browser.find_elements_by_css_selector('div.resume-search-item')
    print(f'current page: {page}, resumes: {len(items)}')
    list(map(process_result_item, items))
    try:
        browser.find_element_by_css_selector('.HH-Pager-Controls-Next').click()
        sleep(2)
    except NoSuchElementException:
        break
    page += 1

browser.close()
print(f'done!')
