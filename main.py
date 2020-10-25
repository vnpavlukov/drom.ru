from files_functions import *
from parsing_functions import *


def main(main_url):
    print('Parse first main page...')

    first_page_response = html_response(main_url, WEB_HEADERS)

    cars_brand_year_power = parse_brand_year_power(first_page_response)
    cars_prices = parse_prices(first_page_response)
    cars_cities = parse_cities(first_page_response)
    cars_urls = parse_urls(first_page_response)

    brand_year_power_prices = []
    for data, price in zip(cars_brand_year_power, cars_prices):
        data['price'] = price
        brand_year_power_prices.append(data)

    brand_year_power_prices_cities = []
    for data, city in zip(brand_year_power_prices, cars_cities):
        data['city'] = city
        brand_year_power_prices_cities.append(data)

    brand_year_power_prices_cities_urls = []
    for data, url in zip(brand_year_power_prices, cars_urls):
        data['url'] = url
        brand_year_power_prices_cities_urls.append(data)

    first_car = 'https://ufa.drom.ru/land_rover/freelander/38618914.html'
    first_car_response = html_response(first_car, WEB_HEADERS)

    car_description_odometer = parse_description_odometer(first_car_response)
    next_url = parse_url_next_page(first_page_response)

    print(car_description_odometer)
    print(next_url)
    print(brand_year_power_prices_cities_urls)


if __name__ == '__main__':

    what_to_parse = input('Парсить УФУ (+200 км, выше 950 тыс) или другой запрос? (д/н)').lower()

    if what_to_parse == 'д':
        main_page = 'https://ufa.drom.ru/auto/all/?minprice=950000&unsold=1&distance=200&order=price'
    else:
        main_page = input('Вставьте ссылку drom.ru с выставленными фильтрами: ')

    print('Start scraping...')
    main(main_page)
