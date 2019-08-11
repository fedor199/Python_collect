import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')
import csv
import pandas as pd

with open('opendata.csv', 'r') as f:
    reader = csv.DictReader(f)
    field_names = reader.fieldnames
    money = []
    date = []
    for row in reader:
        if row['name'] == 'Средняя зарплата' and row['region'] == 'Москва' and '2016-01-01' <= row['date'] <= '2018-12-31':
            region = row['region']
            date.append(row['date'])
            money.append(int(row['value']))
            print(f"На {row['date']} средняя зарплата в регионе {row['region']} соcтавляет {row['value']} рублей")

salary_date = pd.Series(money, index=date)
salary_date.plot(kind='barh')
plt.title(f"Средняя зарплата в регионе {region}", color='red')
plt.show()