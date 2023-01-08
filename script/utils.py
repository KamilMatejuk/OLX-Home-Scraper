from bs4 import BeautifulSoup
from requests.exceptions import ConnectionError
from urllib3.exceptions import MaxRetryError, NewConnectionError
from selenium.common.exceptions import WebDriverException, TimeoutException
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def _get_soup_by(browser, type, value, timeout):
    elements = WebDriverWait(browser, timeout).until(
        EC.presence_of_all_elements_located((
            type, value)
        )
    )
    return [BeautifulSoup(e.get_attribute('innerHTML'), 'html.parser')
            for e in elements]

def get_soup_by_xpath(browser, xpath, timeout=30):
    return _get_soup_by(browser, By.XPATH, xpath, timeout)


def get_soup_by_css_selector(browser, selector, timeout=30):
    return _get_soup_by(browser, By.CSS_SELECTOR, selector, timeout)
