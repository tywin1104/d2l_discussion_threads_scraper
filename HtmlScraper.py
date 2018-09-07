from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


AVENUE_HOME_PAGE_URL = 'http://avenue.mcmaster.ca/?failed=1&authCode=2'


class HtmlScraper:
    def __init__(self, week):
        self.htmls = []
        self.week = week
        self.avenue_home_page = 'http://avenue.mcmaster.ca/?failed=1&authCode=2'
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

        mac_id.send_keys("zhangt73")
        password.send_keys("412476Can*")

        submitButton = self.browser.find_element_by_id("submit")
        submitButton.click()

        all_courses_tab = WebDriverWait(self.browser, 10).until(
                EC.visibility_of_element_located((By.XPATH, "//d2l-tab[@title='All']"))
            )
        all_courses_tab.click()

        # Avenue Dashboard
        cs1jc3_link = WebDriverWait(self.browser, 10).until(
                EC.visibility_of_element_located(
                    (By.XPATH, "//a[@href='/d2l/home/214879']")
                )
        )
        cs1jc3_link.click()

        # # Open Discussion Board
        tabs = self.browser.find_elements_by_css_selector(
            "button.d2l-navigation-s-group.d2l-dropdown-opener"
        )
        communication_tab = tabs[1]
        communication_tab.click()

        try:
            dicussion_tab = WebDriverWait(self.browser, 10).until(
                EC.visibility_of_element_located((By.LINK_TEXT, 'Discussions'))
            )
            dicussion_tab.click()
        except:
            print('Cuold not locate discussion tab')
            self.browser.quit()

        # Open M&M page for specified week
        topic_str = f'M&Ms for Week {self.week}'
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

# Testing
# obj = HtmlScraper(week='03')
# obj.start()

# for index, html in enumerate(obj.htmls):
#     with open(f'page{index}.html', 'w') as fh:
#         fh.write(html)


# from NameCounter import NameCounter
# NameCounter().parse()