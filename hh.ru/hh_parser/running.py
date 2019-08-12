from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from hh_parser import settings
from hh_parser.spiders.hh_ru import HhRuSpider

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)
    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(HhRuSpider)
    process.start()
