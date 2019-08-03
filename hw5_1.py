import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

def request_to_site():
    headers = {
        'accept': '*/*',
        'user-agent': 'User-Agent: Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/'
                      '537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
    }
    try:
        request = requests.get('https://www.avito.ru/moskva/kvartiry/prodam/1-komnatnye?metro=44', headers=headers)
        return request.text
    except requests.exceptions.ConnectionError:
        print('Please check your internet connection!')
        exit(1)

def save_to_mongo_db():
    html_doc = request_to_site()
    soup = BeautifulSoup(html_doc, 'html.parser')
    flats = soup.findAll('div', {'class': 'item_table-header'})
    for flat in flats:
        data_flat = {
            "title": flat.find('a')['title'],
            "addr": flat.findNextSibling('div').find('p', {'class': 'address'}).contents[4],
            "link": f'https://www.avito.ru{flat.find("a")["href"]}',
            "cost": int(flat.find('div').find('span', {'class': 'price'})['content'])
        }
        flats_db.insert_one(data_flat)

def read_from_mongo_db():
    counter = 0
    print('Варианты покупки однокомнатной квартиры в Москве в районе метро Коломенская по возрастанию стоимости')
    my_cost = int(input('Введите максимальную стоимость покупки в рублях: '))
    for flat in flats_db.find({"cost": {"$lt": my_cost}}).sort("cost"):
        counter += 1
        print(f'\nВариант {counter}\nОписание: {flat["title"]},\nАдрес: {flat["addr"][1:]}, \nСсылка: {flat["link"]}\n'
              f'Стоимость: {flat["cost"]} руб.')
    if (counter == 0):
        print('К сожалению,  вариантов с такой стоимостью нет')

client = MongoClient('mongodb://127.0.0.1:27017')
db = client['flats']
flats_db = db.flats
flats_db.drop()
save_to_mongo_db()
read_from_mongo_db()
