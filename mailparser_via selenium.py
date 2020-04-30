from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from pymongo import MongoClient
import time

chrome_options = Options()
chrome_options.add_argument('start-maximized')


driver = webdriver.Chrome('./chromedriver')

driver.get('https://mail.ru')
assert 'Mail.ru' in driver.title

elem = driver.find_element_by_id('mailbox:login')
elem.send_keys('study.ai_172@mail.ru')
elem.send_keys(Keys.RETURN)

time.sleep(1)

elem = driver.find_element_by_id('mailbox:password')
elem.send_keys('NewPassword172')
elem.send_keys(Keys.RETURN)

time.sleep(3)

letter = driver.find_element_by_xpath("//a[1]//div[4]//div[1]//div[3]")
letter.click()

client = MongoClient('localhost', 27017)
db = client['mail_parser']
letters_count = 0

while True:
    letter = {}
    time.sleep(3)
    sender = driver.find_element_by_xpath("//div[@class='letter__author']/span[@class='letter-contact']").text
    date = driver.find_element_by_class_name("letter__date").text
    topic = driver.find_element_by_xpath("//h2[@class='thread__subject thread__subject_pony-mode']").text
    content = driver.find_element_by_class_name("letter-body").text

    letter['sender'] = sender
    letter['date'] = date
    letter['topic'] = topic
    letter['content'] = content

    letters_count += 1

    db.insert_one(letter)

    next_letter = driver.find_element_by_class_name('portal-menu-element_next')
    next_letter.click()

print(f"Было обработано {letters_count} писем")

driver.quit()