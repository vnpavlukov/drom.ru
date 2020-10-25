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

    for car in brand_year_power_prices_cities_urls:
        print('Parse', car['brand_model'], car['year'], 'url:', car['url'])
        first_car_response = html_response(car['url'], WEB_HEADERS)
        car_description_odometer = parse_description_odometer(first_car_response)
        car.update(car_description_odometer)
        sleep(1)

    file_name = file_name_path_data_name_d_m_h()
    write_data_in_file(brand_year_power_prices_cities_urls, file_name)
    json_to_xlsx()

    next_url = parse_url_next_page(first_page_response)
    print(next_url)


if __name__ == '__main__':

    what_to_parse = input('Будем парсить парсить УФУ (+200 км, выше 950 тыс)?\n(д/н): ').lower()

    if what_to_parse in ['д', 'l', 'y']:
        main_page = 'https://ufa.drom.ru/auto/all/?minprice=950000&unsold=1&distance=200&order=price'
    else:
        main_page = input('Вставьте ссылку drom.ru с выставленными фильтрами: ')

    print('Start scraping...')
    main(main_page)
