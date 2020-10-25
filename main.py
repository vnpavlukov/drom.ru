from files_functions import *
from parsing_functions import *

file_name = file_name_path_data_name_d_m_h()


def main(main_url):
    print('Start scraping...')

    if os.path.isfile(file_name):
        print('Some data is already into:', file_name)
        cars_data = get_city_data_from_json_file(file_name)[0]
    else:
        cars_data = dict()

    n = 1
    while True:
        print('Parse', n, 'main page...')

        main_page_response = html_response(main_url, WEB_HEADERS)
        brand_year_power_prices_cities_urls = parse_brand_year_power_prices_cities_urls(main_page_response)

        for key, data in brand_year_power_prices_cities_urls.items():
            if key in cars_data:
                print(data['brand_model'], data['year'], 'in the base')
                continue
            else:
                print('Parse', data['brand_model'], data['year'], 'url:', key)
                car_response = html_response(key, WEB_HEADERS)
                car_description_odometer = parse_description_odometer(car_response)
                data.update(car_description_odometer)
                cars_data.update(data)
                sleep(2)
        write_data_in_file(brand_year_power_prices_cities_urls, file_name)

        next_main_url = parse_url_next_page(main_page_response)
        if not next_main_url:
            print('Это была последняя страница')
            break
        n += 1
        print()


if __name__ == '__main__':

    # what_to_parse = input('Будем парсить парсить УФУ (+200 км, выше 950 тыс)?\n(д/н): ').lower()
    what_to_parse = 'l'
    if what_to_parse in ['д', 'l', 'y']:
        main_page = 'https://ufa.drom.ru/auto/all/?minprice=950000&unsold=1&distance=200&order=price'
    else:
        main_page = input('Вставьте ссылку drom.ru с выставленными фильтрами: ')

    main(main_page)
    # json_to_xlsx()
