import requests
from lxml import html

headers = {'accept': '*/*',
                  'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                'Chrome/75.0.3770.142 Safari/537.36'}
request = 'https://hh.ru/search/vacancy'

def hh_pars(request, headers):
    my_str = input('Please, enter your request here: ')
    session = requests.Session()
    for page in range(0, 3):
        req = session.get(request, headers=headers, params={'text': my_str, 'page': page})
        root = html.fromstring(req.text)
        results = root.xpath(".//a[contains(@class,'bloko-link HH-LinkModifier')]/text()|"
                         ".//div[contains(@class,'vacancy-serp-item__compensation')]/text()|"
                         ".//a[contains(@class,'bloko-link HH-LinkModifier')]/@href")
        if results:
            for i in results:
                print(i)
        else:
            print("At your request no results were found. Please, check your request.")


hh_pars(request, headers)