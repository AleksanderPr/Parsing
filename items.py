import scrapy


class InstaparserItem(scrapy.Item):
    username = scrapy.Field()
    user_id = scrapy.Field()
    folower_username = scrapy.Field()
    folower_id = scrapy.Field()
    folower_photo = scrapy.Field()
    folowwing_username = scrapy.Field()
    folowwing_user_id = scrapy.Field()
    folowwing_photo = scrapy.Field()
    _id = scrapy.Field()
