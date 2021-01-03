import scraper.nike
import scraper.amazon

from scraper.common import ScraperFactory

def init_scrapers(config, drivers):
    return [ScraperFactory.create(drivers, url) for url in config.urls]
