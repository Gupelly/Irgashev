import os
import pandas as pd
from multiprocessing import Pool
import concurrent.futures as cf
import time


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


class Statistics:
    def __init__(self, job, big_file, files_by_years):
        self.job = job
        self.big_file = big_file
        self.files_by_years = files_by_years
        self.result = []

    def year_statistic(self):
        salary_year = {}
        salary_count = {}
        job_salary_year = {}
        job_salary_count = {}
        for year, df in self.files_by_years.items():
            df['salary'] = df[['salary_from', 'salary_to']].mean(axis=1)
            df_job = df[df['name'].str.contains(self.job)]
            salary_year[year] = int(df['salary'].mean())
            salary_count[year] = len(df)
            job_salary_year[year] = int(df_job['salary'].mean())
            job_salary_count[year] = len(df_job)
        return salary_year, salary_count, job_salary_year, job_salary_count

    def one_year_statistic(self, item):
        df = item[1]
        df['salary'] = df[['salary_from', 'salary_to']].mean(axis=1)
        df_job = df[df['name'].str.contains(self.job)]
        return [item[0], int(df['salary'].mean()), len(df), int(df_job['salary'].mean()), len(df_job)]

    def year_statistic_mp(self):
        p = Pool()
        result = p.map(self.one_year_statistic, self.files_by_years.items())

        p.close()
        p.join()

        return {x[0]: x[1] for x in result}, {x[0]: x[2] for x in result}, {x[0]: x[3] for x in result}, {x[0]: x[4] for x in result}

    def year_statistic_with_cf(self):
        result = tuple(cf.ProcessPoolExecutor().map(self.one_year_statistic, self.files_by_years.items()))
        return {x[0]: x[1] for x in result}, {x[0]: x[2] for x in result}, {x[0]: x[3] for x in result}, {x[0]: x[4] for x in result}

    def city_statistic(self):
        total = len(self.big_file)
        self.big_file['salary'] = self.big_file[['salary_from', 'salary_to']].mean(axis=1)
        self.big_file['count'] = self.big_file.groupby('area_name')['area_name'].transform('count')
        df_big = self.big_file[self.big_file['count'] > 0.01 * total].groupby('area_name', as_index=False)

        df_salary_area = df_big['salary'].mean().sort_values(by='salary', ascending=False)
        df_top_salary_area = df_salary_area.head(10)
        top_salary = df_salary_area['salary'].apply(lambda x: int(x))
        salary_by_cities = dict(zip(df_top_salary_area['area_name'], top_salary))

        df_count_area = df_big['count'].mean().sort_values(by='count', ascending=False)
        df_top_count_area = df_count_area.head(10)
        top_cities = df_top_count_area['count'].apply(lambda x: round(x / total, 4))
        count_by_cities = dict(zip(df_top_count_area['area_name'], top_cities))
        return salary_by_cities, count_by_cities

    def print_statistic(self):
        # start_time = time.time()
        # year_data = self.year_statistic()
        # print("--- %s seconds ---" % (time.time() - start_time))

        # start_time = time.time()
        # year_data = self.year_statistic_mp()
        # print("--- %s seconds ---" % (time.time() - start_time))

        start_time = time.time()
        year_data = self.year_statistic_with_cf()
        print("--- %s seconds ---" % (time.time() - start_time))

        city_data = self.city_statistic()
        print(f'Динамика уровня зарплат по годам: {year_data[0]}')
        print(f'Динамика количества вакансий по годам: {year_data[1]}')
        print(f'Динамика уровня зарплат по годам для выбранной профессии: {year_data[2]}')
        print(f'Динамика количества вакансий по годам для выбранной профессии: {year_data[3]}')
        print(f'Уровень зарплат по городам (в порядке убывания): {city_data[0]}')
        print(f'Доля вакансий по городам (в порядке убывания): {city_data[1]}')


if __name__ == '__main__':
    data = DataSet('vacancies_by_year.csv')
    statistic = Statistics('Аналитик', data.file, data.files_by_years)
    statistic.print_statistic()
