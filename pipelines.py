
import scrapy
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline
from pymongo import MongoClient



class LeruaPipeline:
   def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.lerua_base

   def process_item(self, item, spider):
       print()
       collection = self.mongo_base[spider.name]
       collection.insert_one(item)
       return item

class LeruaPhotosPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item['photo']:
            for img in item['photo']:
                try:
                    yield scrapy.Request(img)
                except Exception as e:
                    print(e)


    def item_completed(self, results, item, info):
        item['photo'] = [itm[1] for itm in results if itm[0]]
        return item

#
