import requests
from time import sleep
from bs4 import BeautifulSoup

WEB_HEADERS = {'authority': 'www.domofond.ru', 'cache-control': 'max-age=0',
               'upgrade-insecure-requests': '1',
               'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWeb'
                             'Kit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.11'
                             '6 Safari/537.36',
               'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,'
                         'image/webp,image/apng,*/*;q=0.8,application/signed-'
                         'exchange;v=b3;q=0.9',
               'sec-fetch-site': 'none', 'sec-fetch-mode': 'navigate',
               'sec-fetch-user': '?1', 'sec-fetch-dest': 'document',
               'accept-language': 'en-US,en;q=0.9,ru-RU;q=0.8,ru;q=0.7'}


def html_response(url, headers):
    for _ in range(3):
        try:
            response = requests.get(url, headers=headers)
            return response.text
        except ConnectionError or TimeoutError or ConnectionResetError:
            print("\n*****ConnectionError, TimeoutError or ConnectionResetError*"
                  "****\n\nI will retry again after 7 seconds...")
            sleep(7)
            print('Making another request...')


def parse_brand_year_power(response):
    soup = BeautifulSoup(response, 'html.parser')
    main_page_data = []
    for full_header in soup.find_all('a', class_="css-1hgk7d1 eiweh7o2"):
        split_header = full_header.text.split(', ')
        brand_model = split_header[0]
        year = split_header[1][0:4]
        odometer = split_header[1]

        for i in split_header:
            if 'л.с.' in i:
                power = i.rsplit('(')[-1][:-6]

        main_page_data.append({'brand_model': brand_model, 'year': year, 'power': power})
    return main_page_data


def parse_prices(response):
    soup = BeautifulSoup(response, 'html.parser')
    prices_list = list()
    for price in soup.find_all('span', class_="css-jnatj e162wx9x0"):
        prices_list.append(price.text[:-2])
    return prices_list


def parse_cities(response):
    soup = BeautifulSoup(response, 'html.parser')
    city_list = list()
    for city in soup.find_all('span', class_="css-17qid0e e162wx9x0"):
        city_list.append(city.text.split()[0])
    return city_list


def parse_urls(response):
    soup = BeautifulSoup(response, 'html.parser')
    list_urls = list()
    first = soup.find('div', class_='css-10ib5jr e93r9u20')
    for i in first.find_all('a', class_='css-1hgk7d1 eiweh7o2'):
        list_urls.append(i.get('href'))
    return list_urls


def parse_description(response):
    soup = BeautifulSoup(response, 'html.parser')
    return soup.find('span', class_="css-11eoza4 e162wx9x0").text


def parse_url_next_page(response):
    soup = BeautifulSoup(response, 'html.parser')
    first = soup.find('div', class_='css-se5ay5 e1lm3vns0')

    url = first.find('a', class_='css-1to36mm e24vrp31')
    print(url.get('href'))