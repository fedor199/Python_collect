from pymongo import MongoClient
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

def save_to_mongo_db():
    driver.implicitly_wait(10)
    source = driver.find_elements_by_class_name('ll-crpt')
    theme = driver.find_elements_by_class_name('ll-sj__normal')
    date = driver.find_elements_by_class_name('llc__item_date')
    for item in range(0, 3):
        data_my_mail = {
            "source": source[item].text,
            "theme": theme[item].text,
            "date": date[item].text,
                }
        my_mails_db.insert_one(data_my_mail)
        print("Запись письма в базу данных")


def read_from_mongo_db():
    counter = 0
    print('\nЧтение писем из базы данных')
    for my_mail in my_mails_db.find():
        counter += 1
        print(f'\nПисьмо {counter}\nОт кого: {my_mail["source"]} \nТема письма: {my_mail["theme"]} '
              f'\nДата отправки: {my_mail["date"]}')


driver = webdriver.Chrome()
driver.get('https://mail.ru')
assert "Mail.ru" in driver.title

elem = driver.find_element_by_id("mailbox:login")
elem.send_keys('glushkov-test@inbox.ru')
elem = driver.find_element_by_id("mailbox:password")
elem.send_keys('Asdzxc15')
elem.send_keys(Keys.RETURN)

client = MongoClient('mongodb://127.0.0.1:27017')
db = client['my_mails']
my_mails_db = db.my_mails
my_mails_db.drop()
save_to_mongo_db()

driver.close()

read_from_mongo_db()