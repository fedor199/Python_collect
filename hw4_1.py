import requests
from bs4 import BeautifulSoup


def request_to_site():
    headers = {
        'accept': '*/*',
         'user-agent': 'User-Agent: Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                       ' Chrome/74.0.3729.169 Safari/537.36'
    }
    try:
        request = requests.get('https://news.yandex.ru/Moscow', headers=headers)
        return request.text
    except requests.exceptions.ConnectionError:
        print('Пожалуйста проверьте Интернет соединение!')
        exit(1)


def parse_news():
    html_doc = request_to_site()
    soup = BeautifulSoup(html_doc, 'html.parser')
    cities_news = soup.findAll('h2', {'class': 'story__title'})
    print('Новости из Москвы')
    print('=' * 240)
    for city_news in cities_news:
        print(f'Заголовок: {city_news.find().string}')
        try:
            print(f'Краткое описание: {city_news.findNextSibling("div", {"class": "story__text"}).string}')
        except AttributeError:
            print('Краткое описание: К сожалению, краткого описания нет')
        print(f'Ссылка на новость https://news.yandex.ru{city_news.find()["href"]}')
        print('='*240)

parse_news()
