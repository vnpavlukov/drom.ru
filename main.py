from files_functions import *
from parsing_functions import *

file_name = file_name_path_data_name_d_m_h()


def main(main_url):
    print('Start scraping...')

    if os.path.isfile(file_name):
        print('Some data is already into:', file_name)
        cars_data = get_city_data_from_json_file(file_name)
    else:
        cars_data = dict()

    n = 1
    while True:
        print('Parse', n, 'main page...')

        main_page_response = html_response(main_url, WEB_HEADERS)
        brand_year_power_prices_cities_urls = parse_brand_year_power_prices_cities_urls(main_page_response)

        for car_new_data in brand_year_power_prices_cities_urls:

            print('Parse', car_new_data['brand_model'], car_new_data['year'], 'url:', car_new_data['url'])
            car_response = html_response(car_new_data['url'], WEB_HEADERS)
            car_description_odometer = parse_description_odometer(car_response)
            car_new_data.update(car_description_odometer)
            sleep(1)

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

    main(main_page)
    json_to_xlsx()
