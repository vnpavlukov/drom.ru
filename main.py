from files_functions import *
from parsing_functions import *

MANE_PAGE_YFA = 'https://ufa.drom.ru/auto/all/?minprice=950000&unsold=1&distance=200&order=price'


def main():
    first_page_response = html_response(MANE_PAGE_YFA, WEB_HEADERS)
    brand_year_power = parse_brand_year_power(first_page_response)
    n = 0

    for i in brand_year_power:
        n += 1
        print(n, i)

    cars_prices = parse_prices(first_page_response)
    n = 0
    for i in cars_prices:
        n += 1
        print(n, i)

    brand_year_power_prices = []
    for data, price in zip(brand_year_power, cars_prices):
        data['price'] = price
        brand_year_power_prices.append(data)

    for _ in brand_year_power_prices:
        print(_)

    cities = parse_cities(first_page_response)
    print(cities)

    brand_year_power_prices_cities = []
    for data, city in zip(brand_year_power_prices, cities):
        data['city'] = city
        brand_year_power_prices_cities.append(data)

    for _ in brand_year_power_prices_cities:
        print(_)

    urls = parse_urls(first_page_response)

    n = 0
    for _ in urls:
        n += 1
        print(n, _, end=' ')

    for data, url in zip(brand_year_power_prices, urls):
        data['url'] = url
        brand_year_power_prices_cities.append(data)

    for _ in brand_year_power_prices_cities:
        print(_)

    first_car = 'https://ufa.drom.ru/land_rover/freelander/38618914.html'
    first_car_response = html_response(first_car, WEB_HEADERS)

    car_description = parse_description(first_car_response)
    print(car_description)

    parse_url_next_page(first_page_response)


if __name__ == '__main__':
    main()
