import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem


class SjruSpider(scrapy.Spider):
    name = 'sjru'
    allowed_domains = ['superjob.ru/']
    start_urls = ['https://www.superjob.ru/vacancy/search/?keywords=Python&geo%5Bt%5D%5B0%5D=4']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath('//a[@class="icMQ_ bs_sM _3ze9n _2Pv5x f-test-button-dalshe f-test-link-Dalshe"]/@href').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

        links = response.xpath('//a[contains(@class, "icMQ_ _6AfZ9"]/@href').getall()
        for link in links:
            yield response.follow(link, callback=self.vacancy_parse)




    def vacancy_parse(selfs, response: HtmlResponse):
        name = response.xpath('//h1[@class="rFbjy _2dazi _2hCDz _1RQyC"]/text()').get()
        salary = response.xpath('//span[@class="_2Wp8I _2rfUm _2hCDz"]/text()').getall()
        link = response.url
        item =JobparserItem(name=name, salary=salary, link=link)
        yield item