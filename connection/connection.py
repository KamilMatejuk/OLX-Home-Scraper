from typing import Generator
from requests.exceptions import ConnectionError
from urllib3.exceptions import MaxRetryError, NewConnectionError
from selenium.common.exceptions import WebDriverException, TimeoutException
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import sys
sys.path.append("..")
import const
import logger

    
def get_proxys() -> Generator:
    with open('connection/proxys', 'r') as f:
        proxys = [i.strip() for i in f.readlines() if len(i.strip()) > 0]
        proxys = sorted(list(set(proxys)))
        if len(proxys) == 0:
            while True:
                yield None
        else:
            i = 0
            while True:
                yield proxys[i % len(proxys)]
                i += 1
PROXYS = get_proxys()


class SeleniumConnector():
    def __init__(self, url) -> None:
        self.url = url

    def with_selenium():
        def wrapper(func):
            def inner(self):
                # options
                options = webdriver.ChromeOptions()

                proxy = next(PROXYS) if const.SELENIUM_PROXY else None
                if proxy is not None:
                    options.add_argument(f'--proxy-server={proxy}')

                if const.SELENIUM_HEADLESS:
                    options.add_argument('--headless')
                else:
                    options.add_argument("--start-maximized")

                try:
                    with webdriver.Chrome(
                            executable_path=const.SELENIUM_CHROMEDRIVER,
                            options=options
                        ) as browser:
                        browser.get(self.url)
                        WebDriverWait(browser, 60).until(
                            EC.presence_of_element_located((By.XPATH, '/html/body')))
                        # couldn't load with given IP, proxy error
                        if 'ERR_' in browser.page_source:
                            print(f'\tError: \t page couldn\'t load')
                            return None
                        return func(self, browser)

                except TimeoutException:
                    print(f'\tError: \t{proxy} \t"Too long waiting time"')
                    return None
                except WebDriverException:
                    print(f'\tError: \t{proxy} \t"WebDriverException"')
                    return None
                except (ConnectionError, MaxRetryError, NewConnectionError):
                    print(f'\tError: \t{proxy} \t"Too many requests"')
                    return None
                except KeyboardInterrupt:
                    print()
                    exit(1)
            return inner
        return wrapper
