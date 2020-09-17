import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


AVENUE_HOME_PAGE_URL = 'http://avenue.mcmaster.ca/?failed=1&authCode=2'
COURSE_DISCUSSION_PAGE = 'https://avenue.cllmcmaster.ca/d2l/le/336806/discussions/List'

MAC_ID = os.environ.get('MAC_ID')
PASSWORD = os.environ.get('PASSWORD')

if not MAC_ID or not PASSWORD:
    raise Exception('No env variable set for macid and password')


class HtmlScraper:
    def __init__(self, week):
        self.htmls = []
        self.week = week
        self.browser = None

    def configure(self):
        chromedriver = './chromedriver'
        browser = webdriver.Chrome(chromedriver)
        self.browser = browser

    def to_discussion_page(self):
        if not self.browser:
            raise Exception('Need to configure webdriver first')

        self.browser.get(AVENUE_HOME_PAGE_URL)
        # Login
        login_button = self.browser.find_element_by_id("login_button")
        login_button.click()

        mac_id = self.browser.find_element_by_id("user_id")
        password = self.browser.find_element_by_id("pin")

        mac_id.send_keys(MAC_ID)
        password.send_keys(PASSWORD)

        submitButton = self.browser.find_element_by_id("submit")
        submitButton.click()

        self.browser.get(COURSE_DISCUSSION_PAGE)

        # Open M&M page for specified week
        topic_str = f'Week {self.week} M&Ms'
        mm = self.browser.find_element_by_link_text(topic_str)
        mm.click()

    def iterate_pages(self):
        while True:
            # Sleep 5 seconds for loading all source html
            time.sleep(5)
            html = self.browser.page_source
            self.htmls.append(html)
            next_button = self.browser.find_element_by_xpath("//a[@title='Next Page']")
            if next_button.get_attribute('aria-disabled'):
                break
            else:
                next_button.click()

    def start(self):
        self.configure()
        self.to_discussion_page()
        self.iterate_pages()
