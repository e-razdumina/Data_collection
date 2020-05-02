from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time
from pymongo import MongoClient
import json
import pprint

driver = webdriver.Chrome('./chromedriver')

driver.get('https://www.mvideo.ru/')

assert 'М.Видео' in driver.title

client = MongoClient('localhost', 27017)
db = client['mvideo_parser']
hits_count = 0

time.sleep(5)

products_section = driver.find_element_by_xpath(
        "//body[@class='home']/div[@class='wrapper']/div[@class='page-content']/div[@class='main-holder sel-main-holder']/div[10]/div[1]/div[2]/div[1]/div[1]")

next_page = products_section.find_element_by_class_name("sel-hits-button-next")

while next_page.get_attribute('class') != "next-btn sel-hits-button-next disabled":
    next_page.click()

products = products_section.find_elements_by_xpath(".//a[contains(@class,'sel-product-tile-title')]")

for product in products:
        product_info_str = product.get_attribute("data-product-info")
        product_info = json.loads(product_info_str)
        product_check = db.mvideo.find_one({'productId': product_info['productId']})
        if product_check:
            break
        hits_count += 1
        db.mvideo.insert_one(product_info)

print(f"Была собрана информация о {hits_count} товарах")

driver.quit()
