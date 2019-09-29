# -*- coding: utf-8 -*-
import scrapy
from ico_parser.items import IcoParserItem, PersonItem
from time import sleep


class IcobenchSpider(scrapy.Spider):
    name = 'icobench'
    allowed_domains = ['icobench.com']
    start_urls = ['https://icobench.com/icos?filterSort=name-asc']

    def ico_page_parse(self, response):
        # sleep(0.5)

        site_url = response.css('div.fixed_data div.financial_data a.button_big::attr(href)').get()
        social_urls = response.css('div.fixed_data div.socials a::attr(href)').getall()
        links = [site_url]
        links.extend(social_urls)

        rating = {'Profile': response.xpath('//*[@id="profile_header"]/div/div[2]/div[1]/div/div[2]/div[1]/div/text()').get(),
                  'Team': response.xpath('//*[@id="profile_header"]/div/div[2]/div[1]/div/div[2]/div[2]/div/div/div[1]/text()').get(),
                  'Vision': response.xpath('//*[@id="profile_header"]/div/div[2]/div[1]/div/div[2]/div[2]/div/div/div[2]/text()').get(),
                  'Product': response.xpath('//*[@id="profile_header"]/div/div[2]/div[1]/div/div[2]/div[2]/div/div/div[3]/text()').get()}

        rating_list = []
        ratings_raw = response.xpath('//*[@id="ratings"]/div[2]/div[1]/div[2]')
        for rating_raw in ratings_raw:
            rating = rating_raw.css('div.col_3::text').getall()
            if len(rating) == 3:
                rating_list.append({'Team': rating[0], 'Vision': rating[1], 'Product': rating[2]})
            else:
                # ICO analyzer bot - aggregate all rates
                pass

        people_raw = response.css('#team div.row')
        team = []

        # Found ICOs without team section
        if len(people_raw) > 0:
            team_raw = people_raw[0].css('div.col_3')
            for person_raw in team_raw:
                person_id = person_raw.css('a.image::attr(href)').get()
                person_name = response.css('#team div.row')[0].css('div.col_3')[0].css('a.image::attr(title)').get()
                person_job_title = response.css('#team div.row')[0].css('div.col_3')[0].css('h4::text').get()
                person_links = response.css('#team div.row')[0].css('div.col_3')[0].css('div.socials a::attr(href)').getall()
                person_data = {
                    'url_id': person_id,
                    'name': person_name,
                    'social_links': person_links
                }
                person_item = PersonItem(**person_data)
                team.append({'id':person_id, 'job_title':person_job_title})
                yield person_item

        advisers = []
        # Advisers exists
        if len(people_raw) > 1:
            advisers_raw = people_raw[1].css('div.col_3')
            for person_raw in advisers_raw:
                person_id = person_raw.css('a.image::attr(href)').get()
                person_name = response.css('#team div.row')[0].css('div.col_3')[0].css('a.image::attr(title)').get()
                person_job_title = response.css('#team div.row')[0].css('div.col_3')[0].css('h4::text').get()
                person_links = response.css('#team div.row')[0].css('div.col_3')[0].css('div.socials a::attr(href)').getall()
                person_data = {
                    'url_id': person_id,
                    'name': person_name,
                    'social_links': person_links
                }
                person_item = PersonItem(**person_data)
                advisers.append({'id':person_id, 'job_title':person_job_title})
                yield person_item
        
        preico_time = response.xpath('//*[@id="profile_header"]/div/div[2]/div[3]/div[1]/div/small').get()
        if preico_time is None:
            preico_time_start = response.xpath('//div[@class="col_2" and contains(text(),"preICO start")]//following-sibling::div/b/text()').get()
            preico_time_end = response.xpath('//div[@class="col_2" and contains(text(),"preICO end")]//following-sibling::div/b/text()').get()
            if preico_time_start is not None:
                preico_time = preico_time_start + ' ' + preico_time_end
            else:
                preico_time = 'Unknown'
        ico_time = response.xpath('//*[@id="profile_header"]/div/div[2]/div[3]/div[3]/div/small').get()
        if ico_time is None:
            ico_time_start = response.xpath('//div[@class="col_2" and contains(text(),"ICO start")]//following-sibling::div/b/text()').get()
            ico_time_end = response.xpath('//div[@class="col_2" and contains(text(),"ICO end")]//following-sibling::div/b/text()').get()
            if ico_time_start is not None:
                ico_time = ico_time_start + ' ' + ico_time_end
            else:
                ico_time = 'Unknown'

        price = response.xpath('//div[@class="col_2" and contains(text(),"Price in ICO")]//following-sibling::div/b/text()').get()
        if price is None:
            try:
                price = response.xpath('//div[@class="col_2" and contains(text(),"Price")]//following-sibling::div/b/text()').getall()[1]
            except:
                pass

        data = {
            'name': response.css('div.ico_information div.name h1::text').get(),
            'slogan': response.css('div.ico_information div.name h2::text').get(),
            'description': response.css('div.ico_information p::text').get(),
            'tags': response.css('div.ico_information div.categories a::text').getall(),
            'links': links,
            'rating': rating,
            'rating_list': rating_list,
            'about': '\n'.join(response.css('#about p::text').getall()),
            'team': team,
            'advisers': advisers,
            'preico_time': preico_time,
            'ico_time': ico_time,
            'token': response.xpath('//div[@class="col_2" and contains(text(),"Token")]//following-sibling::div/b/text()').get(),
            'preico_price': response.xpath('//div[@class="col_2" and contains(text(),"PreICO Price")]//following-sibling::div/b/text()').get(),
            'price': price,
            'bonus': response.xpath('//div[@class="col_2" and contains(text(),"Bonus")]//following-sibling::div/b/text()').get(),
            'platform': response.xpath('//div[@class="col_2" and contains(text(),"Platform")]//following-sibling::div/b/text()').get(),
            'investment': response.xpath('//div[@class="col_2" and contains(text(),"Minimum investment")]//following-sibling::div/b/text()').get(),
            'soft_cap': response.xpath('//div[@class="col_2" and contains(text(),"Soft cap")]//following-sibling::div/b/text()').get(),
            'hard_cap': response.xpath('//div[@class="col_2" and contains(text(),"Hard cap")]//following-sibling::div/b/text()').get(),
            'country': response.xpath('//div[@class="col_2" and contains(text(),"Country")]//following-sibling::div/b/text()').get(),
            'whitelist_KYC': response.xpath('//div[@class="col_2" and contains(text(),"Whitelist/KYC")]//following-sibling::div/b/text()').get(),
            'country': response.xpath('//div[@class="col_2" and contains(text(),"Country")]//following-sibling::div/b/text()').get(),
            'restricted_areas': response.xpath('//div[@class="col_2" and contains(text(),"Restricted areas")]//following-sibling::div/b/text()').get()
        }

        item = IcoParserItem(**data)

        yield item        

    def parse(self, response):

        next_page = response.css('div.ico_list div.pages a.next::attr(href)').get()
        ico_pages = response.css('div.ico_list td.ico_data div.content a.name::attr(href)').extract()

        for page in ico_pages:
            yield response.follow(page, callback=self.ico_page_parse)
            # sleep(1)

        yield response.follow(next_page, callback=self.parse)

        print(next_page)