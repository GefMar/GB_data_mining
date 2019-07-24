import scrapy
from time import sleep
from scrapy.selector import Selector
from ico_parser.items import IcoParserItemLoader, IcoParserItem, PersonLoader, Person


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

        l.add_value('socials', list(parse_socials()))
        l.add_value('ratings', float(selector.css('a.view_rating div::text').extract_first()))
        l.add_css('about_section', '#about *')

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

        yield l.load_item()

    def parse(self, response):

        next_page = response.css('div.ico_list div.pages a.next::attr(href)').get()
        ico_pages = response.css('div.ico_list td.ico_data div.content a.name::attr(href)').extract()

        for page in ico_pages:
            yield response.follow(page, callback=self.ico_page_parse)
            # sleep(1)

        yield response.follow(next_page, callback=self.parse)

        print(next_page)
