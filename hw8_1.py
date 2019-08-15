# Итальянская футбольная лига намного популярнее в мире, чем российская. Мне хотелось сравнить стоимости футболистов
# двух этих лиг, чтобы понять коррелирует ли популярность лиг со стоимостью футболистов.
# Программа сравнивает среднюю трансферную стоимость 100 самых дорогих футболистов  российской премьер-лиги и
# итальянской Серии А.  Для построения графика используется возвраст футболистов и средняя трансферная стоимость.
# График показывет, что стоимость футболистов в Италии значительно выше, чем в России (2-5 раз). Это говорит о том, что
# в Италии играют более качественные футболисты и итальянская лига более популярна в мире, чем премьер-лигав Росиии.
# Для анализа использовались данные с сайта  https://www.transfermarkt.ru.


import requests
from lxml import html
import pandas as pd
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')

def parse_country(site_full):
    ages_list = []
    costs_list = []
    headers = {
        'accept': '*/*',
        'user-agent': 'User-Agent: Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/'
                      '537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
    }
    req = requests.get(site_full, headers=headers)
    html_doc = req.text
    root = html.fromstring(html_doc)
    for item  in range(0, 4):
        ages = root.xpath("//tr[contains(@class,'even')]/td[4]/text()|//tr[contains(@class,'odd')]/td[4]/text()")[:25]
        costs = root.xpath("//tr[contains(@class,'even')]/td[contains(@class,'rechts hauptlink')]/span/text()|"
                         "//tr[contains(@class,'odd')]/td[contains(@class,'rechts hauptlink')]/span/text()")[:25]
        for i in range(0,25):
            ages_list.append(int(costs[i].split(',')[0]))
            costs_list.append(int(ages[i]))
        if item == 3:
            break
        site = root.xpath("//li[contains(@class,'naechste-seite')]/a/@href")[0]
        site_full = f'https://www.transfermarkt.ru{site}'
        req = requests.get(site_full, headers=headers)
        html_doc = req.text
        root = html.fromstring(html_doc)
    df = pd.DataFrame({'age': ages_list,'cost': costs_list})
    df = df.loc[df['age'] < 34]
    df_mean = df.groupby('cost')['age'].mean()
    return(df_mean)

def draw_countries(df1, df2):
    plt.title('Сравнение трансферной стоимости футболистов')
    plt.plot(df1, color='green', label='Италия')
    plt.plot(df2, color='red', label='Россия')
    plt.xlabel('Возраст')
    plt.ylabel('Стоимость, млн. евро')
    plt.legend()
    plt.show()

site_russia = 'https://www.transfermarkt.ru/premier-liga/marktwerte/wettbewerb/RU1'
df_russia = parse_country(site_russia)
site_italia = 'https://www.transfermarkt.ru/serie-a/marktwerte/wettbewerb/IT1'
df_italia = parse_country(site_italia)
draw_countries(df_italia, df_russia )
