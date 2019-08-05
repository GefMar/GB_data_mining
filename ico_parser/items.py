# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


# class IcoParserPeople(scrapy.item.Field):
#     team_names = scrapy.Field()
#     team_title = scrapy.Field()
#     team_linkedin = scrapy.Field()
#     name = scrapy.Field()


class IcoParserItem(scrapy.Item):
    _id = scrapy.Field()
    name = scrapy.Field()
    slogan = scrapy.Field()
    description = scrapy.Field()
    tag = scrapy.Field()
    rating = scrapy.Field()
    project_url = scrapy.Field()
    about_project = scrapy.Field()
    # people = IcoParserPeople()
    team = scrapy.Field()
    advisors = scrapy.Field()
    pre_ico_time_begin = scrapy.Field()
    pre_ico_time_end = scrapy.Field()
    ico_time_begin = scrapy.Field()
    ico_time_end = scrapy.Field()
    financial_data = scrapy.Field()

class PersonItem(scrapy.Item):
    _id = scrapy.Field()
    name = scrapy.Field()
    links = scrapy.Field()
    source_page_url = scrapy.Field()


class RatingItem(scrapy.Item):
    overall_rating = scrapy.Field()
    profile_rating = scrapy.Field()
    team_rating = scrapy.Field()
    vision_rating = scrapy.Field()
    product_rating = scrapy.Field()
