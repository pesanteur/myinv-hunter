import getpass
import logging
import os
import pathlib
import random
import re
import requests
import shutil
import string
import subprocess

from abc import ABC, abstractmethod
from selenium import webdriver

user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'

class HttpGetResponse:
    def __init__(self, text, url, **kwargs):
        self.text = text
        self.url = url
        self.status_code = kwargs.get('status_code', None)

class Driver(ABC):
    def __init__(self, **kwargs):
        self.data_dir = kwargs.get('data_dir')
        self.timeout = kwargs.get('timeout')

        @abstractmethod
        def get(self, url) -> HttpGetResponse:
            pass

class SeleniumDriver(Driver):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.selenium_path = pathlib.Path('selenium').resolve()
        self.selenium_path.mkdir(exist_ok=True)
        self.driver_path = self.selenium_path / 'chromedriver'
        driver_paths = [
            '/usr/bin/chromedriver',
            '/usr/local/bin/chromedriver'
        ]
        ### CONTINUE FROM HERE

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
