import pandas as pd
import requests
from xml.etree import ElementTree
from datetime import datetime
from dateutil.relativedelta import relativedelta


class Data:
    def __init__(self, file_name):
        self.df = pd.read_csv(file_name)
        self.currency_dict = {}
        self.get_rate_count()
        self.start_date = self.get_date(range(len(self.df)))
        self.end_date = self.get_date(range(len(self.df) - 1, -1, -1))

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

    def get_date(self, order):
        for i in order:
            if self.df['salary_currency'][i] in self.currency_dict:
                return datetime.strptime(self.df['published_at'][i], '%Y-%m-%dT%H:%M:%S%z').date()


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
            currency_dict = {x: '' for x in currency_list}
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


data = Data('vacancies_dif_currencies.csv')
b = CurrencyData(data.df)
b.get_currency_id(list(data.currency_dict.keys()), data.start_date, data.end_date)


