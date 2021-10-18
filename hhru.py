import scrapy
from scrapy.http import HtmlResponse

from jobparser.items import JobparserItem


class HhruSpider(scrapy.Spider):
    name = 'hhru'
    allowed_domains = ['hh.ru']
    start_urls = ['https://hh.ru/search/vacancy?clusters=true&ored_clusters=true&enable_snippets=true&text=python&area=1&search_field=description&search_field=company_name&search_field=name ',
                  'https://hh.ru/search/vacancy?clusters=true&ored_clusters=true&enable_snippets=true&text=python&area=2&search_field=description&search_field=company_name&search_field=name'] #точки входа

    def parse(self, response: HtmlResponse):
        next_page = response.xpath('//a[@data-qa="pager-next"]/@href').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

        links = response.xpath('//a[@data-qa="vacancy-serp__vacancy-title"]/@href').getall()
        for link in links:
            yield response.follow(link, callback=self.vacancy_parse)




    def vacancy_parse(selfs, response: HtmlResponse):
        name = response.xpath('//h1[@data-qa="vacancy-title"]/text()').get()
        salary = response.xpath('//p[@class="vacancy-salary"]/span/text()').getall()
        link = response.url
        item =JobparserItem(name=name, salary=salary, link=link)
        yield item