from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

# связваем наши локальные файлы с scrappy crawler
from jobparser import settings
from jobparser.spiders.hhru import HhruSpider
from jobparser.spiders.sjru import SjruSpider

if __name__ == '__main__':
    # создаем объект класса Settings
    crawler_settings = Settings()

    #для того чтобы передать ему настройки нашего проекта вызываем метод setmodule и передаем ему импортированный модуль settings
    crawler_settings.setmodule(settings)

    # создаем объект класса для настройки уже самого процесса парсинга
    process = CrawlerProcess(settings=crawler_settings)

    # указываем на то, что процесс будет выполнять наш паук
    process.crawl(HhruSpider)
    process.crawl(SjruSpider)

    process.start()