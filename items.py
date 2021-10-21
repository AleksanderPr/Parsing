
import scrapy
from itemloaders.processors import MapCompose, TakeFirst, Compose

def int_price(value):
    try:
        value = int(value)
    except:
        return value
    return value


class LeruaItem(scrapy.Item):
    name = scrapy.Field(output_processor=TakeFirst())
    link = scrapy.Field(output_processor=TakeFirst())
    price = scrapy.Field(nput_processor=MapCompose(int_price), output_processor=TakeFirst())
    photo = scrapy.Field()
    _id = scrapy.Field()
