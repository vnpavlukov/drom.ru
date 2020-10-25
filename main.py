from files_functions import *
from parsing_functions import *


def main(main_url):
    n = 1
    while True:
        print('Parse', n, 'main page...')

        main_page_response = html_response(main_url, WEB_HEADERS)

        brand_year_power_prices_cities_urls = parse_brand_year_power_prices_cities_urls(main_page_response)

        for car_data in brand_year_power_prices_cities_urls:
            print('Parse', car_data['brand_model'], car_data['year'], 'url:', car_data['url'])
            car_response = html_response(car_data['url'], WEB_HEADERS)
            car_description_odometer = parse_description_odometer(car_response)
            car_data.update(car_description_odometer)
            sleep(1)

        file_name = file_name_path_data_name_d_m_h()
        write_data_in_file(brand_year_power_prices_cities_urls, file_name)

        next_main_url = parse_url_next_page(main_page_response)
        if not next_main_url:
            print('Это была последняя страница')
            break
        n += 1
        print()


if __name__ == '__main__':

    what_to_parse = input('Будем парсить парсить УФУ (+200 км, выше 950 тыс)?\n(д/н): ').lower()

    if what_to_parse in ['д', 'l', 'y']:
        main_page = 'https://ufa.drom.ru/auto/all/?minprice=950000&unsold=1&distance=200&order=price'
    else:
        main_page = input('Вставьте ссылку drom.ru с выставленными фильтрами: ')

    print('Start scraping...')
    main(main_page)
    json_to_xlsx()
