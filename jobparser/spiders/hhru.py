import scrapy
from scrapy.http import HtmlResponse

# Импортируем модуль, где будут храниться собранные данные
from jobparser.items import JobparserItem


class HhruSpider(scrapy.Spider):
    name = 'hhru'
    allowed_domains = ['hh.ru'] # будет работать только по ссылкам доменов, указанных в списке
    start_urls = ['https://hh.ru/search/vacancy?clusters=true&ored_clusters=true&enable_snippets=true&text=python&area=1&search_field=description&search_field=company_name&search_field=name ',
                  'https://hh.ru/search/vacancy?clusters=true&ored_clusters=true&enable_snippets=true&text=python&area=2&search_field=description&search_field=company_name&search_field=name'] #точки входа
    # указываем, что  аргументу response является экземпляром класса HtmlResponse. Благодаря этому в подсказках будут появляться методы этого класса
    def parse(self, response: HtmlResponse):
        #     переход на следующуую страницу
        #     get() позволяет получить один эелемент (достать его из объекта)
        #     в scrapy не обязательно склеивать относительную ссылку с доменом
        # расположено в этом месте для того, чтобы с помощью многопоточности сразу началась обработка следующей страницы
        # и ссылок со следующей страницы при этом паралельно обрабатывалась текущая страница
        next_page = response.xpath('//a[@data-qa="pager-next"]/@href').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)


        # getall() позволяет достать из объекта непосредственно ссылки
        links = response.xpath('//a[@data-qa="vacancy-serp__vacancy-title"]/@href').getall()
        for link in links:
                # yield в отличие от return сохраняет полученное значение после того, как передаст его
                # если бы был return, то цикл for закончился бы при первом круге, а yield позволяет пройти всеь цикл
                # follow выполняет get запрос на указанную ссылку

            #     как только срабатывает функция parse, callback вызывает функцию vacancy_parse, которая уже собирает данные со страницы
            # vacancy_parse без ()
            yield response.follow(link, callback=self.vacancy_parse)




    def vacancy_parse(selfs, response: HtmlResponse):
        name = response.xpath('//h1[@data-qa="vacancy-title"]/text()').get()
        salary = response.xpath('//p[@class="vacancy-salary"]/span/text()').getall()
        link = response.url

        # создаем экземпляр класса JobparserItem и передаем ему информацию о том, куда будут помещаться собранные данные
        item =JobparserItem(name=name, salary=salary, link=link)
        # yield непосредственно возвращает результат
        yield item