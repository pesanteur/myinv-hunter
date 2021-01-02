import getpass
import logging
import os
import requests

from selenium import webdriver

class HttpGetResponse:
    def __init__(self, text, url):
        self.text = text
        self.url = url

class SeleniumDriver:
    def __init__(self, timeout):
        self.timeout = timeout

        self.driver_path = '/usr/bin/chromedriver'
        if not os.path.exists(self.driver_path):
            raise Exception(f'not found: {self.driver_path}')

        self.options = webdriver.ChromeOptions()
        self.options.headless = True
        if getpass.getuser() == 'root':
            self.options.add_argument('--no-sandbox') # required if root

    def get(self, url):
        # headless chromium crashes somewhat regularly...
        # for now, start a frest instance every time
        driver = webdriver.Chrome(self.driver_path, options=self.options)
        try:
            driver.get(url)
            return HttpGetResponse(driver.page_source, url)
        finally:
            driver.close()
            driver.quit()

# Continue from here
