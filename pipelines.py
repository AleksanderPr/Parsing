from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline
from pymongo import MongoClient
import scrapy


class InstaparserPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.db = client.instagram

    def process_item(self, item, spider):
        collection = self.db[spider.name]
        collection.insert_one(item)

        return item