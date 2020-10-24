import os
import json
import pandas
import datetime


def file_name_path_data_name_d_m_h():
    now_day_month_hour = datetime.datetime.today().strftime("%d.%m_%H")
    return os.path.join('data', f"data_cities_{now_day_month_hour}.00.json")


def json_to_xlsx():
    while True:
        is_convert = input('Do you want to convert from json to xlsx (y/n)? ')
        if is_convert == 'y':
            n = 0
            files = []
            for file in os.listdir("data"):
                if file.endswith(".json"):
                    n += 1
                    print(f'{n}. ', file)
                    files.append(file)
            what_file = int(input('Enter the number of the converted file: '))
            json = os.path.join('data', files[what_file - 1])
            xlsx = os.path.join('data', files[what_file - 1][0:-5] + '.xlsx')
            data = pandas.read_json(json, encoding="utf8")
            pandas.DataFrame.transpose(data).to_excel(xlsx)
            print('The converting was successful, have a nice day')
            break
        elif is_convert == 'n':
            print('Have a nice day')
            break


def write_data_in_file(data, name):
    with open(name, 'w', encoding='utf8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    json_to_xlsx()
