'''
1. Выберите веб-сайт с табличными данными, который вас интересует.
2. Напишите код Python, использующий библиотеку requests для отправки HTTP
GET-запроса на сайт и получения HTML-содержимого страницы.
3. Выполните парсинг содержимого HTML с помощью библиотеки lxml, чтобы извлечь данные из таблицы.
4. Сохраните извлеченные данные в CSV-файл с помощью модуля csv.

Ваш код должен включать следующее:

1. Строку агента пользователя в заголовке HTTP-запроса, чтобы имитировать веб-браузер и избежать блокировки сервером.
2. Выражения XPath для выбора элементов данных таблицы и извлечения их содержимого.
3. Обработка ошибок для случаев, когда данные не имеют ожидаемого формата.
4. Комментарии для объяснения цели и логики кода.


Произведем парсинг данных по орбитальным пускам, произведенным РФ и СССР.
Данные по отдельным временным интервалам разнесем в разные csv-файлы.
'''

import requests
from lxml import html
import csv
import time

# Парсинг HTML-содержимого ответа с помощью библиотеки lxml
def parsing_page_data(url):
    response = requests.get(url)
    tree = html.fromstring(response.content)
    return tree

# Функция для скрейпинга табличных данных с одной страницы
def scrape_table_data(url):
    tree = parsing_page_data(url)
    table_rows = tree.xpath("//table[@class='table-launch noborder history']/tr[@valign='top']")

    data = []
    for row in table_rows:
        columns = row.xpath(".//td/text()")
        data.append({
            'number': int(columns[0].strip()), #(columns[0].text.strip()),
            'date': columns[1].strip(),
            'launch_name': row.xpath(".//td[3]/a/text()")[0].strip(),
            'cosmodrome': row.xpath(".//td[4]/a/text()")[0].strip(),
            'booster_rocket': row.xpath(".//td[5]/a/text()")[0].strip(),
            'result': columns[2].strip()
            })
    return data

# Функция для сохранения данных в файл csv
def save_data_to_csv(data, url_end):
    url_end = url_end.replace('-', '_')
    with open(f'starts_{url_end}.csv', 'w', newline='') as file:
        dict_writer = csv.DictWriter(file, data[0].keys())
        dict_writer.writeheader()
        dict_writer.writerows(data)

# Main function
def main():
    url = "https://www.roscosmos.ru/launch/1950/"
    url_1 = "https://www.roscosmos.ru"

    # Определение списка страниц
    tree = parsing_page_data(url)
    url_list = tree.xpath("//span[@class='launch-years']/a/@href") # список относительных url
    years_list = tree.xpath("//span[@class='launch-years']/a/text()") # список годов, соответствующих страницам

    # Обработка каждой страницы, сохранение данных
    for i in range(len(url_list)):
        print(f"Scraping page {url_list[i]}...")
        url = url_1 + url_list[i]
        data = scrape_table_data(url)
        save_data_to_csv(data, years_list[i])
        time.sleep(5)

if __name__ == "__main__":
    main()
