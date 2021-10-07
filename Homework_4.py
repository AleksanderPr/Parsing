from pprint import pprint
from lxml import html
import requests

from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError as dke


headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36'}

url = 'https://lenta.ru'
response = requests.get(url)
dom = html.fromstring(response.text)

# собираем относительные ссылки на новости
short_news_links = dom.xpath("//div[@class='b-yellow-box__wrap']//div[@class='item']/a/@href")

# объединяем относительные ссылки с url и создаем список полных ссылок на новости
list_of_links = []
for short_link in short_news_links:
    news_link = url + short_link
    list_of_links.append(news_link)

all_news = []




# для каждой новости находим ее заголовок и дату публикации
for link in list_of_links:
    news = {}

    news_response = requests.get(link)
    news_dom = html.fromstring(news_response.text)

    # нахождение заголовка новости
    if news_dom.xpath("//h1[@class='b-topic__title']/text()"):
        news_name = news_dom.xpath("//h1[@class='b-topic__title']/text()")
    # оформление одной из новостей отличается от остальных и имеет другой путь к заголовку
    elif news_dom.xpath("//div[@class='premial-header__rubric-wrap']/text()"):
        news_name = news_dom.xpath("//div[@class='premial-header__rubric-wrap']/text()")

    # обработка заголовка для того, чтобы убрать специальные символы
    news_name = str(news_name)
    news_name = news_name.replace('\\xa0', ' ')
    news_name = news_name[2:-2]

    # нахождение даты публикации
    news_date = news_dom.xpath("//div[@class='b-topic__info']/time/text()")
    if news_date:
        news_date = str(news_date)
        news_date = news_date[3:-2]

    # записываем данные в словарь
    news['name'] = news_name
    news['link'] = link
    news['date'] = news_date
    news['sourсe'] = 'Lenta.ru'



    all_news.append(news)


client = MongoClient('127.0.0.1', 27017)
db = client['news']
lenta = db.lenta

for item in all_news:
    try:
        lenta.insert_one({'_id': item['link'],
                          'name': item['name'],
                          'link': item['link'],
                          'data': item['date'],
                          'sourсe': item['sourсe']
                       })
    except dke:
        pass



# Илья, я пытался выполнить пополнение базы данных новыми новостями методом, который Вы показывали при разборе прошлого ДЗ.
# Пытался реализовать это таким образом, но новые новости не добавлялись в базу данных. Ни как не могу поняь,
# что я делаю неправильно?

# for one_news in all_news:
#     if not lenta.find({'link': one_news.get('link')}):
#         lenta.insert_one({'name': one_news['name'],
#                           'link': one_news['link'],
#                           'data': one_news['date'],
#                           'sourсe': one_news['sourсe']
#                        })

#
for doc in lenta.find({}):
    pprint(doc)
