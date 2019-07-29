#Задание 2.
# В приложении парсинга википедии получить первую ссылку на другую страницу и вывести все значимые слова из неё.
# Результат записать в файл в форматированном виде.

import collections
import requests
import re
import xlrd
import xlwt

def return_wiki_html(topic):
    wiki_request = requests.get(f'https://ru.wikipedia.org/wiki/{topic.capitalize()}')
    search_object = re.search('https?:\/\/[a-zA-Z0-9\-\.]+\.[a-zA-Z]{2,3}(\/\S*)?html', wiki_request.text).group()
    print(f' Выбранная ссылка: {search_object}')
    return search_object

def return_words(topic):
    counter = 1
    wiki_html = return_wiki_html(topic)
    http_object = requests.get(wiki_html)
    words = re.findall('[а-яА-Я]{3,}', http_object.text)
    words_counter = collections.Counter()
    for word in words:
        words_counter[word] += 1
    file_ex = xlwt.Workbook()
    sheet_ex = file_ex.add_sheet("Количество слов")
    sheet_ex.write(0, 0, "Cлово")
    sheet_ex.write(0, 1, "Количество")
    for word in words_counter.most_common(20):
        sheet_ex.write(counter,0, word[0])
        sheet_ex.write(counter, 1, word[1])
        counter += 1
    file_ex.save('words_counter.xls')
    print(f'Результат записан в файл: words_counter.xls')

return_words('Война_и_мир')