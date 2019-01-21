# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


# class GetTencentJobScrapyItem(scrapy.Item):
#     # define the fields for your item here like:
#     # name = scrapy.Field()
#     pass


class Tencentitem(scrapy.Item):
    Job_id = scrapy.Field()
    Job_name = scrapy.Field()
    Job_link = scrapy.Field()
    Job_kind = scrapy.Field()
    number = scrapy.Field()
    place = scrapy.Field()
    pubdate = scrapy.Field()
    duty_work = scrapy.Field()
    Job_requirement = scrapy.Field()
