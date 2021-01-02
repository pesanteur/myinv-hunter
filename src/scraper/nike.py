from scraper.common import ScrapeResult, Scraper, ScraperFactory

class NikeScrapeResult(ScrapeResult):
    def parse(self):
        # comb nike page with bs to determine logic here

@ScraperFactory.register
class NikeScraper(Scraper):
    @staticmethod
    def get_domain():
        return 'nike'

    @staticmethod
    def get_driver_type():
        return 'requests' # placeholder before you determine what driver type

    @staticmethod
    def get_result_type():
        return NikeScrapeResult
