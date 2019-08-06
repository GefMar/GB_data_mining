from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from hh_parser import settings
# from hh_parser.spiders.hh import hhSpider
from hh_parser.spiders.selenium_parse_hh import hhSpider

if __name__ == '__main__':

    crawler_settings = Settings()
    crawler_settings.setmodule(settings)
    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(hhSpider)
    process.start()
