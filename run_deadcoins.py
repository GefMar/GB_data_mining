from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from icorating_parser import settings
from icorating_parser.spiders.deadcoins import DeadcoinsSpider

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)
    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(DeadcoinsSpider)
    process.start()
