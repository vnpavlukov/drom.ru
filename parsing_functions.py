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


def parse_brand_year_power_prices_cities_urls(response):
    soup = BeautifulSoup(response, 'html.parser')
    first_data = dict()
    for full_header in soup.find_all('a', class_="css-1hgk7d1 eiweh7o2"):

        split_header = full_header.text.split(', ')
        url = full_header.get('href')
        brand_model = url.split('drom.ru/')[1].split('/')
        brand = brand_model[0]
        model = brand_model[1]
        year = split_header[1][0:4]
        price = full_header.find('span', class_="css-jnatj e162wx9x0").text[:-2]
        city = full_header.find('span', class_="css-17qid0e e162wx9x0").text.split()[0]

        power = None
        for i in split_header:
            if 'л.с.' in i:
                power = i.rsplit('(')[-1][:-6]
        first_data[url] = ({'brand': brand, 'model': model, 'year': year, 'power': power, 'price': price, 'city': city})
    return first_data


def parse_seller_odometer_description(response):
    soup = BeautifulSoup(response, 'html.parser')

    try:
        seller = soup.find('div', class_="css-auda1y e162wx9x0").find('a', class_="css-ioq5yh e1wvjnck0").text
    except AttributeError:
        seller = None

    if not seller:
        try:
            seller = soup.find('div', class_="css-98yt60 e29k6pi2").text
        except AttributeError:
            seller = None

    try:
        description = soup.find('span', class_="css-11eoza4 e162wx9x0").text
    except AttributeError:
        description = None

    odometer = None
    for i in soup.find_all('tr', class_="css-10191hq ezjvm5n2"):
        if 'Пробег' in i.text:
            if 'новый автомобиль' in i.text:
                odometer = 'новый автомобиль'
            else:
                try:
                    odometer = i.text.split('км')[1]
                except:
                    odometer = '??'

    return {'seller': seller, 'odometer': odometer, 'description': description}


def parse_url_next_page(response):
    soup = BeautifulSoup(response, 'html.parser')
    first = soup.find('div', class_='css-se5ay5 e1lm3vns0')
    try:
        return first.find('a', class_='css-1to36mm e24vrp31').get('href')
    except AttributeError:
        return None
