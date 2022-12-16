import pandas as pd
import requests
from xml.etree import ElementTree
from datetime import datetime
from dateutil.relativedelta import relativedelta
from statistics import mean


class Data:
    def __init__(self, file_name):
        self.df = pd.read_csv(file_name)
        self.currency_dict = {}
        self.get_rate_count()
        dates = self.get_date()
        self.start_date = dates[0]
        self.end_date = dates[1]

    def get_rate_count(self):
        for i in range(len(self.df)):
            key = self.df['salary_currency'][i]
            if str(key) == 'nan' or key == 'RUR':
                continue
            if key not in self.currency_dict:
                self.currency_dict[key] = 0
            self.currency_dict[key] += 1
        print(self.currency_dict)
        self.currency_dict = dict([x for x in self.currency_dict.items() if x[1] > 5000])
        self.currency_dict = dict(sorted(self.currency_dict.items(), key=lambda x: x[0]))

    def get_date(self):
        start = datetime.strptime(self.df['published_at'][0], '%Y-%m-%dT%H:%M:%S%z')
        end = start
        for i in range(len(self.df)):
            if self.df['published_at'][i][:4] == '2003' and start > datetime.strptime(self.df['published_at'][i], '%Y-%m-%dT%H:%M:%S%z'):
                start = datetime.strptime(self.df['published_at'][i], '%Y-%m-%dT%H:%M:%S%z')
            if self.df['published_at'][i][:4] == '2022' and end < datetime.strptime(self.df['published_at'][i], '%Y-%m-%dT%H:%M:%S%z'):
                end = datetime.strptime(self.df['published_at'][i], '%Y-%m-%dT%H:%M:%S%z')
        return start.date(), end.date()


class CurrencyData:
    def __init__(self, df):
        self.df = df

    @staticmethod
    def get_year_range(start, end):
        result = []
        start = start + relativedelta(day=1)
        end = end + relativedelta(day=28)
        while start < end:
            result.append(start.strftime('%m/%Y'))
            start = start + relativedelta(months=1)
        return result

    def get_currency_id(self, currency_list, start_date, end_date):
        currency_df = pd.DataFrame(columns=['date'] + currency_list)
        dates = self.get_year_range(start_date, end_date)
        for date in dates:
            url = f'http://www.cbr.ru/scripts/XML_daily.asp?date_req=28/{date}d=1'
            res = requests.get(url)
            res = ElementTree.fromstring(res.content.decode("WINDOWS-1251"))
            currency_dict = {x: None for x in currency_list}
            for valute in res.findall('./Valute'):
                if valute.find('./CharCode').text in currency_list:
                    currency_dict[valute.find('./CharCode').text] = round(float(valute.find('./Value').text.replace(',', '.')) \
                                                                    / int(valute.find('./Nominal').text), 4)
                    if all(currency_dict.values()):
                        break
            currency_dict = sorted(currency_dict.items(), key=lambda x: x[0])
            currency = [x[1] for x in currency_dict]
            currency_df.loc[len(currency_df.index)] = [date] + currency
        currency_df.to_csv('currency.csv', index=False)
        return currency_df


class NewCsv:
    def __init__(self, original_df, currency_df):
        self.original_df = original_df
        self.currency_df = currency_df

    def create_new_csv(self, range):
        new_df = pd.DataFrame(columns=['name', 'salary', 'area_name', 'published_at'])
        for i in range:
            salary = None
            currency = 1
            row = list(self.original_df.loc[i])
            salary_list = list(filter(lambda x: str(x) != 'nan', row[1:3]))
            if len(salary_list) != 0:
                salary = mean(salary_list)
            if row[3] != 'RUR':
                if row[3] in list(self.currency_df.columns):
                    currency = self.currency_df[self.currency_df['date'] == datetime.strptime(row[5], '%Y-%m-%dT%H:%M:%S%z').strftime('%m/%Y')][row[3]].iloc[0]
            if salary is not None and currency is not None:
                salary = round(salary * currency)
            if salary is None or currency is None:
                salary = None
            new_df.loc[len(new_df)] = [row[0]] + [salary] + row[4:6]
        new_df.to_csv('new_csv.csv', index=False)


data = Data('vacancies_dif_currencies.csv')
currency_data = CurrencyData(data.df)
currency_csv = currency_data.get_currency_id(list(data.currency_dict.keys()), data.start_date, data.end_date)
new_csv = NewCsv(data.df, currency_csv)
new_csv.create_new_csv(range(100))


