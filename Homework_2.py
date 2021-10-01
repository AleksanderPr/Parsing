import requests
import json
from pprint import pprint
from bs4 import BeautifulSoup as bs
import pandas as pd


url = 'https://hh.ru'
full_url = 'https://hh.ru/search/vacancy?clusters=true&ored_clusters=true&enable_snippets=true&st=searchVacancy&' \
           'text=Python&from=suggest_post&search_field=description&search_field=company_name&search_field=name'
params = {
    'clusters': 'true',
    'ored_clusters': 'true',
    'enable_snippets': 'true',
    'st': 'searchVacancy',
    'text': 'Python',
    'from': 'suggest_post',
    'search_field': ['description', 'company_name', 'name']
}

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36'}



vacacies = []

while True:

    # response = requests.get(url + '/search/vacancy', params=params, headers=headers)
    # complex_url =
    response = requests.get(full_url, params=params, headers=headers)
    soup = bs(response.text, 'html.parser')
    vacancy_list = soup.find_all('div', attrs={'class': 'vacancy-serp-item'})

    for vacancy in vacancy_list:
        vacancy_data = {}
        # vacancy_info = vacancy.find('span', attrs={'class': 'g-user-content'})
        vacancy_name = vacancy.find('span', attrs={'class': 'g-user-content'}).text
        vacancy_link = vacancy.find('a', attrs={'class': 'bloko-link'})['href']
        site_sourсe = url
        salary_line = vacancy.find('div', attrs={'class': 'vacancy-serp-item__row vacancy-serp-item__row_header'})
        salary_info = vacancy.find('span', attrs={'data-qa': 'vacancy-serp__vacancy-compensation'})

        min_salary = None
        max_salary = None
        currency = None

        if salary_info:
            salary = salary_info.text
            salary = salary.split(' ')
            if salary[0] == 'от':
                min_salary = salary[1]
                max_salary = None
                currency = salary[2]
            elif salary[0] == 'до':
                min_salary = None
                max_salary = salary[1]
                currency = salary[2]
            else:
                min_salary = salary[0]
                max_salary = salary[2]
                currency = salary[3]

        if min_salary:
            min_salary = min_salary.replace('\u202f', '')
            min_salary = float(min_salary)

        if max_salary:
            max_salary = max_salary.replace('\u202f', '')
            max_salary = float(max_salary)

        vacancy_data['name'] = vacancy_name
        vacancy_data['min_salary'] = min_salary
        vacancy_data['max_salary'] = max_salary
        vacancy_data['currency'] = currency
        vacancy_data['link'] = vacancy_link
        vacancy_data['site_sourсe'] = site_sourсe

        vacacies.append(vacancy_data)

    next = soup.find('a', attrs={'data-qa': 'pager-next'})

    if next:
        full_url = url + next['href']
    else:
        break





df = pd.DataFrame(vacacies)
df.to_excel('vacacies.xlsx')
df.to_csv('vacacies.csv')

pprint(vacacies)

