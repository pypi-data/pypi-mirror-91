__author__ = 'Vinicius wovst @ viniciuswovst in GitHub'
__version__ = '1.0'

# Copyright 2020-2021 Vinicius Wovst, viniciuswovst @ GitHub
# See LICENSE for details.

from bs4 import BeautifulSoup

import requests
import pandas as pd
from datetime import date, datetime

class Reuters:
    BASE_URL = 'https://www.reuters.com/companies/api'
        
    def _get_data(self, ticker, report_name, yearly=True):
        url = '%s/getFetchCompanyFinancials/%s' % (self.BASE_URL, ticker)
        #headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'}
        #, headers=headers    
        
        req = requests.get(url)
        result = {}
        if req.status_code == 200:
            content = req.json()
            market_data = content['market_data']
            market_data = market_data['financial_statements']
            income = market_data[report_name]
            if (yearly):
                result = income['annual']
            else:
                result = income['interim']

        return result

    def _format_data(self, ticker, report_name, metric, ticker_values, yearly):
        list_values = []
        today = date.today()
        for periodo in ticker_values:
            date_periodo = datetime.strptime(periodo['date'], '%Y-%m-%d').date()
            year = date_periodo.year
            valor = periodo['value']

            ticker_values = {
                'dataAtual':str(today),
                'nomeAcao':ticker,
                'relatorioFinanceiro': report_name,
                'fonte':'reuters',
                'ano':year,
                'metrica':metric,
                'valor':valor
                }
            if not(yearly):
                trimestre = {'trimestre': (date_periodo.month-1)//3+1}
                ticker_values.update(trimestre)
            list_values.append(ticker_values)
        return list_values


    def get_income_statement(self, ticker_list, yearly=True):
        list_values = []
        for ticker in ticker_list:
            income = self._get_data(ticker, 'income', yearly)
            metricas = income.keys()

            for item in metricas:
                metrica = item
                periodos = income[item]
                list_values = list_values+self._format_data(ticker, 'income_statement', metrica, periodos, yearly)
        df = pd.DataFrame (list_values)
        return df

    
    def get_cash_flow(self, ticker_list, yearly=True):
        list_values = []
        for ticker in ticker_list:
            income = self._get_data(ticker, 'cash_flow', yearly)
            metricas = income.keys()

            for item in metricas:
                metrica = item
                periodos = income[item]
                list_values = list_values+self._format_data(ticker, 'cash_flow', metrica, periodos, yearly)
        df = pd.DataFrame (list_values)
        return df

    def get_balance_sheet(self, ticker_list, yearly=True):
        list_values = []
        for ticker in ticker_list:
            income = self._get_data(ticker, 'balance_sheet', yearly)
            metricas = income.keys()

            for item in metricas:
                metrica = item
                periodos = income[item]
                list_values = list_values+self._format_data(ticker, 'balance_sheet', metrica, periodos, yearly)
        df = pd.DataFrame (list_values)
        return df

    def get_fields_date(self, ticker):
        fields_date = {}
        req_ws = requests.get('https://www.reuters.com/companies/api/getFetchCompanyKeyMetrics/%s' % ticker)
        DATE_MASK = '%Y-%m-%dT%H:%M:%S'
        if req_ws.status_code == 200:
            content_ws = req_ws.json()['market_data']
            fields_date = {
                'Pricing date':datetime.strptime(content_ws['price_date'], DATE_MASK).date(),
                '52 Week High Date':datetime.strptime(content_ws['fiftytwo_week_high_date'], DATE_MASK).date(),
                '52 Week Low Date':datetime.strptime(content_ws['fiftytwo_week_low_date'], DATE_MASK).date()
            }
        return fields_date

    def get_key_metrics(self, ticker_list):
        today = date.today()
        list_values = []
        for ticker in ticker_list:
            req = requests.get('https://www.reuters.com/companies/%s/key-metrics'% ticker)

            fields_date = self.get_fields_date(ticker)

            if req.status_code == 200:
                content = req.content
                soup = BeautifulSoup(content, 'lxml')
                div_table = soup.find_all(name='div', attrs={'class':'KeyMetrics-table-container-3wVZN'})
                for div in div_table:
                    report_name = div.find_all(name='h3')[0].text
                    tr_list = div.find_all(name='tr')
                    for tr in tr_list:
                        metric = tr.find_all(name='th')[0].text
                        value = tr.find_all(name='td')[0].text

                        if len(value) == 0:
                            value = fields_date[metric]

                        ticker_values = {
                            'dataAtual':str(today),
                            'nomeAcao':ticker,
                            'fonte':'reuters',
                            'metrica':metric,
                            'valor':value,
                            'relatorio_financeiro':report_name
                            }
                        list_values.append(ticker_values)

        df = pd.DataFrame (list_values)
        return df        
