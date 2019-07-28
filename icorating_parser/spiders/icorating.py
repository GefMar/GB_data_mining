# -*- coding: utf-8 -*-
import scrapy
from icorating_parser.items import IcoratingParserItem
import json
from time import sleep


class IcoratingSpider(scrapy.Spider):
    api_url = 'https://icorating.com/ico/all/load/?page={}&sort=investment_rating&direction=desc'
    name = 'icorating'
    allowed_domains = ['icorating.com']
    start_urls = [api_url.format(1)]
    current_page = 1
    last_page = 0

    def ico_page_parse(self, response):

        name = response.xpath('//h1[@class = "c-heading c-heading--big"]/text()').get().strip()
        area = response.xpath('//div[@class = "o-media__body o-media__body--center ml15"]/p/text()').get().strip()
        invest_rating = response.xpath('//span[@itemprop = "ratingValue"]/text()').get().strip()
        hype_score = response.xpath('//span[@class = "c-card-info__name" and contains(text(), "Hype score")]/following-sibling::*/text()').get().strip()
        risk_score = response.xpath('//span[@class = "c-card-info__name" and contains(text(), "Risk score")]/following-sibling::*/text()').get().strip()
        links = response.xpath('//div[@class = "c-social-icons c-social-icons--grey c-social-icons--center mb15 mt10"]/a/@href').getall()

        if len(response.xpath('//div[@class = "mb15"]').getall()) > 0:
            overview = ' '.join(response.xpath('//div[@class = "mb15"]//text()').getall()).strip()
        else:
            overview = 'N/A'

        if len(response.xpath('//div[@class = "mb25"]').getall()) > 0:
            feats = ' '.join(response.xpath('//div[@class = "mb25"]//text()').getall()).strip()
        else:
            feats = 'N/A'

        if response.xpath('//th[@class = "c-card-info__cell"]/text()').re('Start ICO'):
            start_ico = response.xpath('//th[@class = "c-card-info__cell" and contains(text(), "Start ICO")]/following-sibling::*/text()').get().strip()
        else:
            start_ico = 'N/A'

        if response.xpath('//th[@class = "c-card-info__cell"]/text()').re('End ICO'):
            end_ico = response.xpath('//th[@class = "c-card-info__cell" and contains(text(), "End ICO")]/following-sibling::*/text()').get().strip()
        else:
            end_ico = 'N/A'

        team_members_count = response.xpath('count(//h3[@class = "c-heading c-heading--small mb10" and contains(text(), "Team members")]/following-sibling::div[1]//tbody[@class = "c-table__body"]/tr)').get()
        advisors_count = response.xpath('count(//h3[@class = "c-heading c-heading--small mb10" and contains(text(), "Team members")]/following-sibling::div[2]//tbody[@class = "c-table__body"]/tr)').get()

        team_members = []
        for i in range(1, int(float(team_members_count))+1):
            team_members.append({
                'name': response.xpath('//h3[@class = "c-heading c-heading--small mb10" and contains(text(), "Team members")]/following-sibling::div[1]//tbody/tr[$index]//div[@class = "o-media__image visible-medium"]/a/@title', index=i).get(),
                'link': response.xpath('//h3[@class = "c-heading c-heading--small mb10" and contains(text(), "Team members")]/following-sibling::div[1]//tbody/tr[$index]//div[@class = "o-media__image visible-medium"]/a/@href', index=i).get(),
                'position': response.xpath('//h3[@class = "c-heading c-heading--small mb10" and contains(text(), "Team members")]/following-sibling::div[1]//tbody/tr[$index]//td[2]/text()', index=i).get().strip(),
                'social': response.xpath('//h3[@class = "c-heading c-heading--small mb10" and contains(text(), "Team members")]/following-sibling::div[1]//tbody/tr[$index]//div[@class = "c-social-icons"]/a/@href', index=i).getall()
            })

        advisors = []
        for i in range(1, int(float(advisors_count))+1):
            advisors.append({
                'name': response.xpath('//h3[@class = "c-heading c-heading--small mb10 mt20" and contains(text(), "Advisors")]/following-sibling::div[1]//tbody/tr[$index]//div[@class = "o-media__image visible-medium"]/a/@title', index=i).get(),
                'link': response.xpath('//h3[@class = "c-heading c-heading--small mb10 mt20" and contains(text(), "Advisors")]/following-sibling::div[1]//tbody/tr[$index]//div[@class = "o-media__image visible-medium"]/a/@href', index=i).get(),
                'position': response.xpath('//h3[@class = "c-heading c-heading--small mb10 mt20" and contains(text(), "Advisors")]/following-sibling::div[1]//tbody/tr[$index]//td[2]/text()', index=i).get().strip(),
                'social': response.xpath('//h3[@class = "c-heading c-heading--small mb10 mt20" and contains(text(), "Advisors")]/following-sibling::div[1]//tbody/tr[$index]//div[@class = "c-social-icons"]/a/@href', index=i).getall()
            })

        data = {
            'name': name,
            'area': area,
            'overview': overview,
            'feats': feats,
            'start_ico': start_ico,
            'end_ico': end_ico,
            'invest_rating': invest_rating,
            'hype_score': hype_score,
            'risk_score': risk_score,
            'links': links,
            'team_members': team_members,
            'advisors': advisors
        }

        item = IcoratingParserItem(**data)
        yield item

    def parse(self, response):

        if self.current_page == 3:
            print('Current page: {}. Exit!'.format(self.current_page))
            return
        else:
            print('Current page: {}. Let\'s  parse something!'.format(self.current_page))
            data = json.loads(response.text)
            self.last_page = data['icos']['last_page']

        for item in data['icos'].get('data'):
            sleep(0.5)
            print(item['link'])
            yield response.follow(item['link'], callback=self.ico_page_parse)

        self.current_page += 1
        next_page = self.api_url.format(self.current_page+1)
        yield response.follow(next_page, callback=self.parse)


