from unittest import TestCase
from full import Salary, Vacancy, VacancyForStatistics


class SalaryTests(TestCase):
    def test_salary_type(self):
        self.assertEqual(type(Salary(['10', '20', 'True', 'RUR'])).__name__, "Salary")

    def test_salary_from(self):
        self.assertEqual(Salary(['10', '20', 'True', 'RUR']).salary_from, 10)

    def test_salary_to(self):
        self.assertEqual(Salary(['10', '20', 'True', 'RUR']).salary_to, 20)

    def test_salary_currency(self):
        self.assertEqual(Salary(['10', '20', 'True', 'RUR']).salary_currency, "RUR")

    def test_average_salary(self):
        self.assertEqual(Salary(['10', '20', 'True', 'RUR']).average_salary, 15)

    def test_average_salary_with_currency(self):
        self.assertEqual(Salary(['10', '20', 'True', 'USD']).average_salary, 909.9)


class VacancyTests(TestCase):
    def test_type(self):
        self.assertEqual(type(Vacancy(['Аналитик', 'Аналитик', 'Аналитик', 'noExperience', 'False', 'Аналитик',
                                       '10', '20', 'True', 'RUR', 'Москва', '2022-06-14T11:44:58+0300'] )).__name__, 'Vacancy')

    def test_descr(self):
        descr = 'a' * 1000
        self.assertEqual(len(Vacancy(['Аналитик', descr, 'Аналитик', 'noExperience', 'False', 'Аналитик',
                                       '10', '20', 'True', 'RUR', 'Москва', '2022-06-14T11:44:58+0300']).translate_vacancy()[1]), 103)
        self.assertEqual(Vacancy(['Аналитик', descr, 'Аналитик', 'noExperience', 'False', 'Аналитик',
                                      '10', '20', 'True', 'RUR', 'Москва',
                                      '2022-06-14T11:44:58+0300']).translate_vacancy()[1][100:103], '...')

    def test_exp_translate(self):
        self.assertEqual(Vacancy(['Аналитик', 'Аналитик', 'Аналитик', 'noExperience', 'False', 'Аналитик',
                                  '10', '20', 'True', 'RUR', 'Москва',
                                  '2022-06-14T11:44:58+0300']).translate_vacancy()[3], 'Нет опыта')

    def test_bool_translate(self):
        self.assertEqual(Vacancy(['Аналитик', 'Аналитик', 'Аналитик', 'noExperience', 'False', 'Аналитик',
                                  '10', '20', 'True', 'RUR', 'Москва',
                                  '2022-06-14T11:44:58+0300']).translate_vacancy()[4], 'Нет')

    def test_salary_type(self):
        self.assertEqual(type(Vacancy(['Аналитик', 'Аналитик', 'Аналитик', 'noExperience', 'False', 'Аналитик',
                                  '10', '20', 'True', 'RUR', 'Москва',
                                  '2022-06-14T11:44:58+0300']).salary).__name__, 'Salary')

    def test_date(self):
        self.assertEqual(Vacancy(['Аналитик', 'Аналитик', 'Аналитик', 'noExperience', 'False', 'Аналитик',
                                  '10', '20', 'True', 'RUR', 'Москва',
                                  '2022-06-14T11:44:58+0300']).translate_vacancy()[8], '14.06.2022')


class VacancyForStatisticsTests(TestCase):
    def test_type(self):
        self.assertEqual(type(VacancyForStatistics(['Аналитик', '10', '20', 'RUR', 'Москва', '2022-06-14T11:44:58+0300'])).__name__, 'VacancyForStatistics')

    def test_year(self):
        self.assertEqual(VacancyForStatistics(['Аналитик', '10', '20', 'RUR', 'Москва', '2022-06-14T11:44:58+0300']).year, 2022)

    def test_salary(self):
        self.assertEqual(VacancyForStatistics(['Аналитик', '10.5', '21.5', 'RUR', 'Москва', '2022-06-14T11:44:58+0300']).salary, 16)

    def test_salary_with_currency(self):
        self.assertEqual(VacancyForStatistics(['Аналитик', '10.5', '21.5', 'USD', 'Москва', '2022-06-14T11:44:58+0300']).salary, 970.56)

