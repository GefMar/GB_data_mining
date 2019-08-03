from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from ico_parser import settings
# from ico_parser.spiders.icobench import IcobenchSpider
from ico_parser.spiders.icorating import IcoratingSpider

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)
    process = CrawlerProcess(settings=crawler_settings)
    # process.crawl(IcobenchSpider)
    process.crawl(IcoratingSpider)
    process.start()
