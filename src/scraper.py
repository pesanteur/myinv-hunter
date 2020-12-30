import locale
import logging
import pathlib
import random
import re

from bs4 import BeautifulSoup

class ScrapeResult:
    def __init__(self, r):
        self.alert_subject = None
        self.alert_content = None
        self.price = None
        self.soup = BeautifulSoup(r.text, 'lxml')
        self.content = self.soup.body.text.lower() # lower for case-insensitive searches
        self.url = url

    def __bool__(self):
        return bool(self.alert_content)

    def has_phrase(self, phrase):
        return phrase in self.content

    def set_price(self, tag):
        if not tag:
            return

        price_str = tag.text.strip()
        if not price_str:
            return

        try:
            currency_symbol = locale.localeconv()['currency_symbol']
            self.price = locale.atof(price_str.replace(currency_symbol, '').strip())
            return price_str if price_str else None
        except Exception as e:
            logging.warning(f'unable to convert "{price_str}" to float... caught exception: {e}')


class GenericScrapeResult(ScrapeResult):
    def __init__(self, r):
        super().__init__(r)

        # not perfect but usually good enough
        if self.has_phrase('add to cart'):
            self.alert_subject = 'In Stock'
            self.alert_content = self.url

def get_result_type(url):
    return GenericScrapeResult # add other scraper result types

def get_short_name(url):
    parts = [i for i in url.path.split('/') if i]
    if parts:
        return '_'.join(parts) # add other short name results
    random.seed()
    return f'unknown{random.randrange(100)}'

class Scraper:
    def __init__(self, driver, url):
        self.driver = driver
        self.name = get_short_name(url)
        self.result_type = get_result_type(url)
        self.url = url
        self.in_stock_on_last_scrape = False
        self.price_on_last_scrape = None

        data_dir = pathlib.Path('data').resolve()
        data_dir.mkdir(exist_ok=True)
        self.filename = data_dir / f'{self.name}.txt'
        logging.info(f'scraper initialized for {self.url}')

    def scrape(self):
        try:
            url = str(self.url)
            r = self.driver.get(url)
            with self.filename.open('w') as f:
                f.write(r.text)
            return self.result_type(r)

        except Exception as e:
            logging.error(f'{self.name}: caught exception during request: {e}')
