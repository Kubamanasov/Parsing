import csv
import requests
from bs4 import BeautifulSoup # -> всю инфо с сайта структурирует под себя,  и позволять работать со своими методами



def get_html(url): #  ->  тут сканирует весь сайт, вытаскиет данные и возвращает их в виде строки 
    response = requests.get(url)
    return response.text


def get_total_pages(html): # -> получаем url и находим последнию страницу
    soup = BeautifulSoup(html, 'lxml')
    pages_ul = soup.find('nav').find('ul', class_='pagination').find_all('li')[-1].find('a').get('href').split('=')[-1]
    return int(pages_ul)

def write_to_csv(boss):  # -> вес отсоритрованные данные в конце тут записывает в csv файл
    with open('mashinakg3.csv', 'a') as f1:
        writer = csv.writer(f1, delimiter='/')
        writer.writerow((boss['title'],
                         boss['price'],
                         boss['photo'],
                         boss['opis']))

def get_page_data(html): # -> тут нахожу целую таблицу и структурирую для дальнейшей работы
    soup = BeautifulSoup(html, 'lxml')
    products = soup.find('div', class_='table-view-list').find_all('div', class_='list-item')
    
    for product in products:
        #photo, title, price, opis

        photo = product.find('div', class_='thumb-item-carousel').find('img').get('data-src')
        title = product.find('h2').text.replace('  ', '').replace('\n', ' ')
        price = product.find('p', class_='price').text.replace('  ', '').replace('\n', '.')
        opis = product.find('div', class_='item-info-wrapper').text.strip().replace('\n', ' ').replace('    ', '')

        boss = {'title': title, 'price': price, 'photo': photo, 'opis': opis}
        write_to_csv(boss)

def main():
    cars_url = 'https://www.mashina.kg/search/all/'
    pages = '?page='
    total_pages = get_total_pages(get_html(cars_url))
    
    
    for page in range(1, 5):
        alle = cars_url + pages + str(page)
        html = get_html(alle)
        get_page_data(html)

main()  