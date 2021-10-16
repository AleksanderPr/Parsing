# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class JobparserItem(scrapy.Item):
    # define the fields for your item here like:
    # записываем сода поля, которые будут храниться
    # name = scrapy.Field()
    name = scrapy.Field()
    salary_min = scrapy.Field()
    salary_max = scrapy.Field()
    currency = scrapy.Field()
    salary = scrapy.Field()
    link = scrapy.Field()
    # для записи в Mongo обязательно создать поле _id
    _id = scrapy.Field()