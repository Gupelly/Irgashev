import os
import pandas as pd


class DataSet:

    def __init__(self, file_name):
        self.file = self.csv_filter(file_name)
        path = r'C:\Users\user\Irgashev\years'
        for f in os.listdir(path):
            os.remove(os.path.join(path, f))
        self.files_by_years = self.get_folders(self.file)

    @staticmethod
    def csv_filter(file_name):
        df = pd.read_csv(file_name)
        if len(df) == 0:
            return print('Пустой файл')
        if len(df) == 1:
            return print('Нет данных')
        return df

    @staticmethod
    def get_folders(df):
        if df is None:
            return
        df['years'] = df['published_at'].apply(lambda x: int(x[:4]))
        years = df['years'].unique()
        files_by_year = {}
        for year in years:
            data = df[df['years'] == year]
            year_file = data[['name', 'salary_from', 'salary_to', 'salary_currency', 'area_name', 'published_at']]
            files_by_year[year] = year_file
            year_file.to_csv(rf'years\{year}.csv', index=False)
        return files_by_year


data = DataSet(input('Введите название файла: '))

