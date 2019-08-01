import scrapy
from time import sleep
from scrapy.selector import Selector
from ico_parser.items import IcoParserItemLoader, IcoParserItem, PersonLoader, Person
import datetime
import re

class IcobenchSpider(scrapy.Spider):
    name = 'icobench'
    allowed_domains = ['icobench.com']
    start_urls = ['https://icobench.com/icos?filterSort=name-asc']

    def ico_page_parse(self, response):
        selector = Selector(response)
        l = IcoParserItemLoader(IcoParserItem(), response)
        l.add_css('name', 'div.ico_information div.name h1::text')
        l.add_css('slogan', 'div.ico_information div.name h2::text')
        l.add_css('description', 'div.ico_information p::text')
        l.add_css('categories', 'div.categories a::text')
        l.add_css('site', '.button_big::attr(href)')

        def parse_socials():
            for e in selector.css('.fixed_data .socials a'):
                yield {
                    'title': e.css('::attr(title)').extract_first(),
                    'href':  e.css('::attr(href)').extract_first()
                }

        def parse_ratings():
            yield {
                'profile': ''.join(selector.xpath("//span[@class='label_top notranslate']/../text()[2]").re(r'\d+.\d+')),
                'team': ''.join(selector.xpath("//span[@class='label_top']/following-sibling::div[@class='columns']/div[1]").re(r'\d+.\d+')),
                'vision': ''.join(selector.xpath("//span[@class='label_top']/following-sibling::div[@class='columns']/div[2]").re(r'\d+.\d+')),
                'product': ''.join(selector.xpath("//span[@class='label_top']/following-sibling::div[@class='columns']/div[3]").re(r'\d+.\d+'))
            }

        l.add_value('socials', list(parse_socials()))
        l.add_value('ratings', parse_ratings())
        l.add_css('about_section', '#about *')

        def parse_iso_times():
            ico_times = selector.xpath("//div[@class='financial_data']/div[@class='divider']/preceding-sibling::div[@class='row']")
            ico_times.reverse()

            tmp_ico_times = {}

            try:

                tmp_ico_times['ico'] = [datetime.datetime.strptime(date, '%Y-%m-%d')
                                        for date in
                                        ico_times[0].xpath('descendant::small//text()').get().split(' - ')]

                if len(ico_times) > 1:
                    tmp_ico_times['preico'] = [datetime.datetime.strptime(date, '%Y-%m-%d')
                                               for date in
                                               ico_times[1].xpath('descendant::small//text()').get().split(' - ')]
            except (IndexError, AttributeError):
                pass

            yield tmp_ico_times

        l.add_value('iso_times', parse_iso_times())

        def load_person(element):
            l = PersonLoader(Person(), element)
            l.add_css('profile', 'a.image::attr(href)')
            l.add_css('name', 'h3::text')
            l.add_css('job', 'h4::text')
            l.add_value('socials', element.css('div.socials a::attr(href)').extract())
            return l.load_item()

        def parse_team():
            team = {
                'team': [],
                'advisors': []
            }
            for e in selector.css('#team h2 + a + .row .col_3'):
                team['team'].append(load_person(e))
            for e in selector.css('#team h3 + .row .col_3'):
                team['advisors'].append(load_person(e))

            return team

        l.add_value('team', parse_team())
        #l.add_value('whitepaper', selector.css('div#whitepaper object::attr(data)').extract_first() or "None")
        l.add_css('whitepaper', 'div#whitepaper object::attr(data)')

        def parse_financial_data():
            financial_data = {}
            data_rows = selector.xpath("//div[@class='financial_data']/div[@class='data_row']")
            for row in data_rows:
                key = re.sub("^\s+|\s+$", "", row.xpath("descendant::div[1]/text()").get(), flags=re.UNICODE)
                financial_data[key] = re.sub("^\s+|\s+$", "", row.xpath("descendant::div[2]/b//text()").get(), flags=re.UNICODE)

            yield financial_data

        l.add_value('financial_data', parse_financial_data())

        yield l.load_item()

    def parse(self, response):

        next_page = response.css('div.ico_list div.pages a.next::attr(href)').get()
        ico_pages = response.css('div.ico_list td.ico_data div.content a.name::attr(href)').extract()

        for page in ico_pages:
            yield response.follow(page, callback=self.ico_page_parse)
            # sleep(1)

        yield response.follow(next_page, callback=self.parse)

        print(next_page)
