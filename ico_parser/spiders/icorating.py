# -*- coding: utf-8 -*-
import scrapy
from ico_parser.items import PersonItem, IcoRatingItem
from time import sleep
import json

class IcoratingSpider(scrapy.Spider):
    name = 'icorating'
    allowed_domains = ['icorating.com']
    current_page = 1
    start_urls = ['https://icorating.com/ico/all/load/?page=1&sort=name&direction=asc']

    def get_url(self):
        return f'https://icorating.com/ico/all/load/?page={self.current_page}&sort=name&direction=asc'

    def ico_page_parse(self, response):

        team = []
        team_raw = response.xpath('//*[@id="team"]/h3[contains(text(),"Team members")]//following-sibling::div/table/tbody/tr')
        if len(team_raw) > 0:
            for person_raw in team_raw:
                links = person_raw.xpath('.//img//parent::a/@href').getall()
                person_id = links[0]
                person_name = person_raw.xpath('.//img//parent::a/@title').get()
                person_job_title = person_raw.xpath('.//td[2]/text()').get().strip()
                person_links = links[1:]
                person_data = {
                    'url_id': person_id,
                    'name': person_name,
                    'social_links': person_links
                }
                person_item = PersonItem(**person_data)
                team.append({'id':person_id, 'job_title':person_job_title})
                yield person_item

        advisers = []
        advisers_raw = response.xpath('//*[@id="team"]/h3[contains(text(),"Advisors")]//following-sibling::div/table/tbody/tr')
        if len(advisers_raw) > 1:
            for person_raw in advisers_raw:
                links = person_raw.xpath('.//img//parent::a/@href').getall()
                person_id = links[0]
                person_name = person_raw.xpath('.//img//parent::a/@title').get()
                person_job_title = person_raw.xpath('.//td[2]/text()').get().strip()
                person_links = links[1:]
                person_data = {
                    'url_id': person_id,
                    'name': person_name,
                    'social_links': person_links
                }
                person_item = PersonItem(**person_data)
                advisers.append({'id':person_id, 'job_title':person_job_title})
                yield person_item

        data = {
            'name': response.xpath('//*[@id="ico-card"]/div[1]/div[1]/div[1]/div[2]/h1/text()').get(),
            'description': response.xpath('//*[@id="ico-card"]/div[1]/div[1]/div[3]/p/text()').get(),
            'links': response.xpath('//*[@id="ico-card"]/div[1]/div[1]/div[2]/div/span[contains(text(),"Share")]//following-sibling::a/@href').getall(),
            'investment_rating': response.xpath('//*[@id="ico-card"]/div[1]/div[2]/div[1]/div[1]/span[3]/text()').get(),
            'hype_score': response.xpath('//*[@id="ico-card"]/div[1]/div[2]/div[1]/div[2]/span[2]/text()').get(),
            'risk_score': response.xpath('//*[@id="ico-card"]/div[1]/div[2]/div[1]/div[3]/span[2]/text()').get(),            
            'team': team,
            'advisers': advisers,
            'ico_time_start': response.xpath('//*[@id="ico-card"]/div[1]/div[2]/div[3]/table[2]/tbody/tr[1]/td/text()').get(),
            'ico_time_end': response.xpath('//*[@id="ico-card"]/div[1]/div[2]/div[3]/table[2]/tbody/tr[2]/td/text()').get()
        }

        item = IcoRatingItem(**data)

        yield item   
    
    def parse(self, response):        
        self.current_page += 1
        next_page = self.get_url()

        jsonresponse = json.loads(response.body_as_unicode())

        for page in jsonresponse['icos']['data']:
            yield response.follow(page['link'], callback=self.ico_page_parse)

        if self.current_page <= jsonresponse['icos']['last_page']:
            yield response.follow(next_page, callback=self.parse)

            print(next_page)