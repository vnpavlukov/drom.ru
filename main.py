from files_functions import *
from parsing_functions import *

# file_name = file_name_path_data_name_d_m_h()
file_name = os.path.join('data', f"data_drom.ru_25.10_23.00.json")

def main(main_url):
    print('Start scraping...')

    if os.path.isfile(file_name):
        print('Some data is already into:', file_name)
        cars_data = get_city_data_from_json_file(file_name)
    else:
        cars_data = dict()

    page = 1
    while True:
        print('Parse', page, 'page...')

        main_page_response = html_response(main_url, WEB_HEADERS)
        brand_year_power_prices_cities_urls = parse_brand_year_power_prices_cities_urls(main_page_response)

        n = 1
        for key_url, data in brand_year_power_prices_cities_urls.items():
            if key_url in cars_data and 'description' in cars_data[key_url]:
                print(n, data['brand_model'], data['year'], 'in the base')
                n += 1
            else:
                print(n, 'Parse', data['brand_model'], data['year'], 'url:', key_url)

                car_response = html_response(key_url, WEB_HEADERS)
                car_description_odometer = parse_odometer_description(car_response)
                brand_year_power_prices_cities_urls[key_url].update(car_description_odometer)
                cars_data.update(brand_year_power_prices_cities_urls)
                sleep(1)
                n += 1

        write_data_in_file(cars_data, file_name)

        main_url = parse_url_next_page(main_page_response)
        if not main_url:
            print('Это была последняя страница')
            break
        page += 1
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
