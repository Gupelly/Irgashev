import math
import pandas as pd
import requests
from xml.etree import ElementTree
from datetime import datetime
from dateutil.relativedelta import relativedelta
from statistics import mean
import concurrent.futures as cf
from multiprocessing import Pool


class NewCsv:
    def __init__(self, original_df, currency_df):
        self.original_df = original_df
        self.currency_df = currency_df

    def create_one_csv(self, df):
        new_df = pd.DataFrame(columns=['name', 'salary', 'area_name', 'published_at'])
        for i in range(len(df)):
            salary = None
            currency = 1
            row = list(df.loc[i])
            print(row[6])
            salary_list = list(filter(lambda x: not math.isnan(x), row[1:3]))
            if len(salary_list) != 0:
                salary = mean(salary_list)
            if row[3] != 'RUR':
                if row[3] in list(self.currency_df.columns):
                    currency = self.currency_df[self.currency_df['date'] == row[5][:7]][row[3]].iloc[0]
            if salary is not None and currency is not None:
                salary = round(salary * currency)
            if salary is None or currency is None:
                salary = None
            new_df.loc[len(new_df)] = [row[0]] + [salary] + row[4:6]
        new_df.to_csv(rf'more_years\{len(df)}.csv', index=False)

    def create_all_csv(self):
        self.original_df['years'] = self.original_df['published_at'].apply(lambda x: int(x[:4]))
        years = self.original_df['years'].unique()
        df_list = [self.original_df[self.original_df['years'] == x] for x in years]
        df_list = [df.reset_index(drop=True) for df in df_list]
        # for df in df_list:
        #     print(df)
        #     self.create_one_csv(df)
        cf.ProcessPoolExecutor().map(self.create_one_csv, tuple(df_list))


if __name__ == '__main__':
    data = pd.read_csv('vacancies_dif_currencies.csv')
    currency_csv = pd.read_csv('currency.csv')
    new_csv = NewCsv(data, currency_csv)
    # new_csv.create_one_csv(1000)
    new_csv.create_all_csv()
