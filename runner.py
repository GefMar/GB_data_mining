import os
from os.path import join, dirname
from dotenv import load_dotenv
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from jobparser import settings
from jobparser.spiders.hhru import HhruSpider
from jobparser.spiders.instagram import InstagramSpider
from jobparser.spiders.superjob import SuperjobSpider
from jobparser.spiders.avito import AvitoSpider
from jobparser.spiders.zillow import ZillowSpider
from jobparser.spiders.autoru import AutoruSpider

do_env = join(dirname(__file__), '.env')
load_dotenv(do_env)

INST_LOGIN = os.getenv('INST_LOGIN')
INST_PWD = os.getenv('INST_PASSWORD')

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)
    process = CrawlerProcess(settings=crawler_settings)
    # process.crawl(HhruSpider)
    process.crawl(ZillowSpider)
    # process.crawl(SuperjobSpider)
    # process.crawl(InstagramSpider, ['geekbrains', 'harleydavidson'], INST_LOGIN, INST_PWD)
    process.start()
