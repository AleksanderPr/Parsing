import requests
import json
from pprint import pprint



url = 'https://api.stockdata.org/v1/data/eod'
company = ['AAPL', 'TSLA', 'GAZP.ME']
for i in company:
    my_params = {
        'symbols': i,
        # 'api_token': 'pass',
        'date_from': '2021-09-01',
        'date_to': '2021-09-03'
    }

    req = requests.get(url, params=my_params)
    json_req = req.json()
    f_fson = json.loads(req.text)
    meta = json_req.get('meta')
    data = json_req.get('data')
    for i in data:
        print(f"Акция: {meta.get('name')}, дата торгов: {i.get('date')}, цена закрытия: {i.get('close')}")

    with open("stock_file.json", "a") as write_file:
        json.dump(f_fson, write_file)