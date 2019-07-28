# Задание 1.
# Доработать приложение по поиску авиабилетов, чтобы оно возвращало билеты по названию города, а не по IATA коду.
# Пункт отправления и пункт назначения должны передаваться в качестве параметров.
# Сделать форматированный вывод, который содержит в себе пункт отправления, пункт назначения, дату вылета, цену билета.



import requests
import json
import sys

if __name__ == "__main__":
    if len (sys.argv) == 3:
        src = sys.argv[1]
        dst = sys.argv[2]
    else:
        if len(sys.argv) < 3:
            print (f'Ошибка! Слишком мало параметров, должно быть два')
            sys.exit (1)

        if len(sys.argv) > 3:
            print(f'Ошибка! Слишком много параметров, должно быть два')
            print(sys.argv[1], sys.argv[2])
            sys.exit(1)

string = src + ' ' + dst
flight_params = {'q': string}


req = requests.get("https://www.travelpayouts.com/widgets_suggest_params", params=flight_params)

data = req.json()

try:
    flight_params = {
    'origin': data['origin']['iata'],
    'destination': data['destination']['iata'],
    'one_way': 'true'
}
except KeyError:
    print(f'Ошибка! Вы неправильно ввели параметры, пункты отправления и назначения должны быть на русском языке')
    print(f'Пример правильного запроса: "python hw2_1.py Москва Лондон"')
    sys.exit(1)

req = requests.get("http://min-prices.aviasales.ru/calendar_preload", params=flight_params)
data = req.json()
tickets = data['best_prices']
for ticket in tickets:
    print(f' Пункт отправления: {src}, пункт назначения: {dst}, дата вылета: {ticket["depart_date"]}, '
          f'цена билета: {ticket["value"]}')