# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

# импортируем монго
from pymongo import MongoClient


class JobparserPipeline:
    # создаем указание на базу данных
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.vacancy16_10




    def process_item(self, item, spider):
        # item['salary_min'], item['salary_max'], item['currency'] = self.process_salary(item['salary'])
        if spider.name == 'hhru':
            item['salary_min'], item['salary_max'], item['currency'] = self.hhprocess_salary(item['salary'])
            del item['salary']
        if spider.name == 'sjru':
            item['salary_min'], item['salary_max'], item['currency'] = self.sjprocess_salary(item['salary'])
            del item['salary']
        # сохраняем в коллекцию монго под именем названия паука
        collection = self.mongo_base[spider.name]
        collection.insert_one(item)
        return item



    # функция для обработки зарплаты
    def hhprocess_salary(self, salary):
        # salary_min = None
        # salary_max = None
        # currency = None

        # salary = salary.split(' ')
        if salary[0] == 'от':
            salary_min = salary[1]
            salary_max = None
            currency = salary[2]
        elif salary[0] == 'до':
            salary_min = None
            salary_max = salary[1]
            currency = salary[2]
        else:
            salary_min = salary[0]
            salary_max = salary[2]
            currency = salary[3]

        # if salary_min:
        #     salary_min = salary_min.replace('\u202f', '')
        #     salary_min = float(salary_min)
        #
        # if salary_max:
        #     salary_max = salary_max.replace('\u202f', '')
        #     salary_max = float(salary_max)

        return salary_min, salary_max, currency


    def sjprocess_salary(self, salary):
        # salary_min = None
        # salary_max = None
        # currency = None

        # salary = salary.split(' ')
        if salary[0] == 'от':
            salary_min = salary[1]
            salary_max = None
            currency = salary[2]
        elif salary[0] == 'до':
            salary_min = None
            salary_max = salary[1]
            currency = salary[2]
        else:
            salary_min = salary[0]
            salary_max = salary[2]
            currency = salary[3]

        if salary_min:
            salary_min = salary_min.replace('&nbsp', '')
            salary_min = float(salary_min)

        if salary_max:
            salary_max = salary_max.replace('&nbsp', '')
            salary_max = float(salary_max)

        return salary_min, salary_max, currency
