
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import time
from bs4 import BeautifulSoup as Soup
from selenium.common.exceptions import NoSuchElementException

class Scrape_by_Crawler:
    def __init__(self):
        self.chromedriver_path = './chromedriver'


    def drive_engine_init(self):
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        driver = webdriver.Chrome(self.chromedriver_path,chrome_options=chrome_options)
        return driver


    def query_target_location(self, driver, url=None):
        # go to target location website
        driver.get(url)
        return driver


    def scroll_to_down(self, driver, run_num):
        # scroll on website
        run_num, run = 10, 0
        while run <= run_num:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)
            try:
                driver.find_element_by_class_name('section-loading').click()
                time.sleep(1)
            except NoSuchElementException:
                a = 0
            finally:
                run +=1
        return driver


    def crawling_for_location_name(self, driver):
        soup = Soup(driver.page_source,"lxml")
        all_reviews = soup.find_all(class_ = 'section-hero-header-title-title gm2-headline-5')
        loc_name = ''
        for ar in all_reviews:
            loc_name += ar
        return driver, loc_name


    def main(self, target_location_url, driver):
        # go to target location website
        driver = self.query_target_location(driver, target_location_url)
        driver = self.scroll_to_down(driver, run_num=10)
        # dynamic search
        run_key, index = True, 0
        while run_key is True:
            # click one of relative location
            diff_loc_button = driver.find_elements_by_class_name("place-result-container-place-link")
            if index >= len(diff_loc_button):
                break
            diff_loc_button[index].click()
            time.sleep(10)
            # get target location name
            driver, loc_name = self.crawling_for_location_name(driver)
            # click more review button
            driver.find_elements_by_class_name("widget-pane-link")[0].click()
            time.sleep(5)
            driver = self.scroll_to_down(driver, run_num=10)
            # extend all content for each reiview
            extend_content_button = driver.find_elements_by_class_name("section-expand-review.mapsConsumerUiCommonButton__blue-link")
            for extend_content_unit_button in extend_content_button:
                extend_content_unit_button.click()
            # static crawling
            driver = self.static_crawling(driver)
            index += 1


    def static_crawling(self, driver):
        soup = Soup(driver.page_source,"lxml")
        user_class = 'section-review mapsConsumerUiCommonRipple__ripple-container gm2-body-2'
        all_reviews = soup.find_all(class_ = user_class)  
        for ar in all_reviews:
            review_user_name = ar.find(class_ = "section-review-title").text
            subtitle_review = ar.find(class_ = "section-review-text").text
            star_review = str(ar.find(class_ = "section-review-stars").get('aria-label').strip().strip("顆星"))
            date_review = ar.find(class_ = "section-review-publish-date").text
            text_review = ar.find(class_ = "section-review-text").text
            # print('review_user_name : ',review_user_name)
            # print('subtitle_review : ',subtitle_review)
            # print('star_review : ',star_review)
            # print('date_review : ',date_review)
            # print('text_review : ',text_review)
            # print('----------------------------------')
        #print('=========================================')
        driver.back()
        time.sleep(3)
        driver.back()
        time.sleep(3)
        return driver


    def forward(self, target_location_url=None):
        driver = self.drive_engine_init()
        self.main(target_location_url, driver)



if __name__ == '__main__':
    target_location_url='https://www.google.com.tw/maps/search/%E7%8E%8B%E5%93%81%E7%89%9B%E6%8E%92/'
    SBC_obj = Scrape_by_Crawler()
    SBC_obj.forward(target_location_url)
