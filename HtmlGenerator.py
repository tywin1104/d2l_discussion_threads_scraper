from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

chromedriver = './chromedriver'
brower = webdriver.Chrome(chromedriver)
brower.get('http://avenue.mcmaster.ca/?failed=1&authCode=2')

# Enter login page
login_button = brower.find_element_by_id("login_button")
login_button.click()

mac_id = brower.find_element_by_id("user_id")
password = brower.find_element_by_id("pin")

mac_id.send_keys("zhangt73")
password.send_keys("412476Can*")

submitButton = brower.find_element_by_id("submit")
submitButton.click()

# Enter Dashboard
try:
    cs1jc3_link = WebDriverWait(brower, 10).until(
        EC.presence_of_element_located((By.XPATH , "//a[@href='/d2l/home/214879']"))
    )
    cs1jc3_link.click()
except:
    print('Cuold not locate cs1jc3 course page')
    brower.quit()

# Open Discussion Board
tabs = brower.find_elements_by_css_selector("button.d2l-navigation-s-group.d2l-dropdown-opener")
communication_tab = tabs[1]
communication_tab.click()

try:
    dicussion_tab = WebDriverWait(brower, 10).until(
        EC.presence_of_element_located((By.LINK_TEXT , 'Discussions'))
    )
    dicussion_tab.click()
except:
    print('Cuold not locate discussion tab')
    brower.quit()

time.sleep(5)
brower.close()