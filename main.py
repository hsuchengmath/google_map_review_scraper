

import os
import re
import time
import pandas as pd
from datetime import datetime
from selenium import webdriver
from bs4 import BeautifulSoup as Soup
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver

driver = webdriver.Chrome('./chromedriver')
main_url = 'https://www.google.com.tw/maps/search/%E7%8E%8B%E5%93%81%E7%89%9B%E6%8E%92/'
# go to website given restaurant
driver.get(main_url)
time.sleep(5)

# scroll up to go dowm
run_num, run = 10, 0
while run <= run_num:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    run +=1
# differnet location given restaurant
run_key, index = True, 0
while run_key is True:
    diff_loc_button = driver.find_elements_by_class_name("place-result-container-place-link")
    if index >= len(diff_loc_button):
        break
    unit_button = diff_loc_button[index]
    unit_button.click()
    time.sleep(10)
    # click more review button
    load_more_review_button = driver.find_elements_by_class_name("widget-pane-link")[0]
    load_more_review_button.click()
    time.sleep(5)
    # scroll up all review
    run_num, run = 10, 0
    while run <= run_num:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        driver.find_element_by_class_name('section-loading').click()
        time.sleep(1)
        run +=1
    # extend all content for each reiview
    extend_content_button = driver.find_elements_by_class_name("section-expand-review.mapsConsumerUiCommonButton__blue-link")
    for extend_content_unit_button in extend_content_button:
        extend_content_unit_button.click()
    print('need extend content num : ',len(extend_content_button))
    # show review
    soup = Soup(driver.page_source,"lxml")
    user_class = 'section-review mapsConsumerUiCommonRipple__ripple-container gm2-body-2'
    all_reviews = soup.find_all(class_ = user_class)    
    print('all reviews num:',len(all_reviews))
    for ar in all_reviews:
        review_user_name = ar.find(class_ = "section-review-title").text
        subtitle_review = ar.find(class_ = "section-review-text").text
        star_review = str(ar.find(class_ = "section-review-stars").get('aria-label').strip().strip("顆星"))
        date_review = ar.find(class_ = "section-review-publish-date").text
        text_review = ar.find(class_ = "section-review-text").text
        print('review_user_name : ',review_user_name)
        print('subtitle_review : ',subtitle_review)
        print('star_review : ',star_review)
        print('date_review : ',date_review)
        print('text_review : ',text_review)
        print('----------------------------------')
    print('=========================================')
    driver.back()
    time.sleep(3)
    driver.back()
    time.sleep(3)
    index += 1

