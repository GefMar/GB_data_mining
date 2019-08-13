# -*- coding: utf-8 -*-
import scrapy
from ico_parser.items import IcoParserItem, PersonItem


class IcobenchSpider(scrapy.Spider):
    name = 'icobench'
    allowed_domains = ['icobench.com']
    start_urls = ['https://icobench.com/icos?filterSort=name-asc']

    def ico_page_parse(self, response):
        # Условие для обработки проектов, которые ведут на стартовую страницу
        if response.xpath('//div[@id="browse"]/div[@class="frame"]/h2/text()').getall() != ['Browse ICOs']:

            def socials_parse():
                names = response.css('div.socials a::text').extract()
                links = response.css('div.socials a::attr(href)').extract()
                return dict(zip(names, links))

            def rating_parse():
                ratings = {'profile': None,
                           'team': None,
                           'vision': None,
                           'product': None
                           }

                tmp_profile = response.xpath('//div[@class="distribution"]//div[@class="wrapper" and '
                                             '//span/text()="Benchy"]/text()').re(r'\d+.\d+|-')
                try:
                    ratings['profile'] = float(tmp_profile[0]) if tmp_profile else None
                except:
                    pass

                tmp_expert_rating = response.xpath(
                    '//div[@class="distribution"]//div[@class="columns"]/div[@class="col_4 col_3"]/text()').re(
                    r'\d.\d|-')

                if tmp_expert_rating:
                    for i, itm in enumerate(tmp_expert_rating):
                        try:
                            tmp_expert_rating[i] = float(itm)
                        except:
                            tmp_expert_rating[i] = None

                    ratings['team'] = tmp_expert_rating[0]
                    ratings['vision'] = tmp_expert_rating[1]
                    ratings['product'] = tmp_expert_rating[2]
                return ratings

            def about_parse():
                about_string = ''
                about_all = response.css('div#profile_content div#about p::text').extract()
                for about in about_all:
                    about_string = about_string + about + ' '
                return about_string.rstrip()

            data_persons = response.css('div.tab_content#team div.row')

            try:

                team = [
                    {
                        'person': PersonItem(
                            person_url=itm.css('a::attr(href)').get(),
                            name=itm.css('h3::text').get(),
                            social_links=itm.css('div.socials a::attr(href)').extract()),
                        'position': itm.css('h4::text').get()
                    }
                    for itm in data_persons[0].css('div.col_3')
                ]


            except IndexError as error:
                # print(error)
                team = []

            try:
                advisors = [
                    {
                        'person': PersonItem(
                            person_url=itm.css('a::attr(href)').get(),
                            name=itm.css('h3::text').get(),
                            social_links=itm.css('div.socials a::attr(href)').extract()),
                        'position': itm.css('h4::text').get()
                    }
                    for itm in data_persons[1].css('div.col_3')
                ]

                try:
                    for itm in data_persons[2].css('div.col_3'):
                        tmp_person = {
                            'person': PersonItem(
                                person_url=itm.css('a::attr(href)').get(),
                                name=itm.css('h3::text').get(),
                                social_links=itm.css('div.socials a::attr(href)').extract()),
                            'position': itm.css('h4::text').get()
                        }
                        advisors.append(tmp_person)

                except:
                    pass

            except IndexError as error:
                # print(error)
                advisors = []


            tmp_preico_time = response.xpath('//div[@class="financial_data"]//div[@class="col_2 expand"]/'
                                                 'label[contains(text(), "PreICO time")]/../small/text()').getall()
            preico_time = tmp_preico_time[0] if tmp_preico_time else None


            tmp_ico_time = response.xpath('//div[@class="financial_data"]//div[@class="col_2 expand"]/'
                                          'label[contains(text(), "ICO Time")]/../small/text()').getall()
            ico_time = tmp_ico_time[0] if tmp_ico_time else None

            tmp_status = response.xpath(
                '//div[@class="financial_data"]/div[@class="row"]//div[@class="number"]/text()').getall()
            status = tmp_status[0] if tmp_status else None

            fin_data_key = response.xpath(
                '//div[@class="financial_data"]//div[@class="data_row"]/div[1]/text()').re(r'\w+.\w*.\w+')
            fin_data_value = response.xpath(
                '//div[@class="financial_data"]//div[@class="data_row"]/div[2]/b//text()').getall()

            financial_data = dict(zip(fin_data_key, fin_data_value))

            data = {'name': response.css('div.ico_information div.name h1::text').get().lstrip(),
                    'slogan': response.css('div.ico_information div.name h2::text').get(),
                    'description': response.css('div.ico_information p::text').get(),
                    'categories': response.css('div.categories a::text').extract(),
                    'official_link': response.css('div.financial_data a.button_big::attr(href)').get(),
                    'project_social_links': socials_parse(),
                    'ratings': rating_parse(),
                    'experts_ratings': rating_parse(),
                    'about': about_parse(),
                    'team': team,
                    'advisors': advisors,
                    'preico_time': preico_time,
                    'ico_time': ico_time,
                    'status': status,
                    'token': financial_data.get('Token'),
                    'type': financial_data.get('Type'),
                    'preico_price': financial_data.get('PreICO Price'),
                    'price': financial_data.get('Price'),
                    'bonus': financial_data.get('Bonus'),
                    'bounty': financial_data.get('Bounty'),
                    'mvp_prototype': financial_data.get('MVP/Prototype'),
                    'platform': financial_data.get('Platform'),
                    'accepting': financial_data.get('Accepting'),
                    'minimum_investment': financial_data.get('Minimum investment'),
                    'soft_cap': financial_data.get('Soft cap'),
                    'hard_cap': financial_data.get('Hard cap'),
                    'country': financial_data.get('Country'),
                    'whitelist_kyc': financial_data.get('Whitelist/KYC'),
                    'restricted_areas': financial_data.get('Restricted areas'),
                    'price_in_ico': financial_data.get('Price in ICO'),
                    'ico_start': financial_data.get('ICO start'),
                    'ico_end': financial_data.get('ICO end'),
                    }

            item = IcoParserItem(**data)

        else:
            item = IcoParserItem()

        yield item

    def parse(self, response):
        next_page = response.css('div.ico_list div.pages a.next::attr(href)').get()
        ico_pages = response.css('div.ico_list td.ico_data div.content a.name::attr(href)').extract()

        for page in ico_pages:
            yield response.follow(page, callback=self.ico_page_parse)

        yield response.follow(next_page, callback=self.parse)

        print(next_page)
