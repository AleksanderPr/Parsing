from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from lerua import settings
from lerua.spiders.lerua_spider import LeruaSpiderSpider

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)
    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(LeruaSpiderSpider, query='плитка')

    process.start()