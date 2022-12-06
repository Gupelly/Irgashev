import os
import csv


def csv_reader(file_name):
    file_csv = open(file_name, encoding='utf_8_sig')
    reader_csv = csv.reader(file_csv)
    list_data = list(filter(lambda x: '' not in x, reader_csv))
    if len(list_data) == 0:
        return print('Пустой файл')
    if len(list_data[1:]) == 0:
        return print('Нет данных')
    return list_data[0], list_data[1:]


data = csv_reader('vacancies_by_year.csv')
title = data[0]
vacancies = data[1]
path = r'C:\Users\user\Irgashev\years'
if not os.path.exists(path):
    os.makedirs(path)
for f in os.listdir(path):
    os.remove(os.path.join(path, f))

n = 0
while n < len(vacancies):
    year = vacancies[n][5].split('-')[0]
    file_name = year + '.csv'
    file = open(file_name, 'a', newline='', encoding="utf-8")
    writer = csv.writer(file)
    writer.writerow(title)
    while n < len(vacancies) and year == vacancies[n][5].split('-')[0]:
        writer.writerow(vacancies[n])
        n += 1
    file.close()
    os.replace(file_name, 'years\\' + file_name)

