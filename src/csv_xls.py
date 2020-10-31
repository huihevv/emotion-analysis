import pandas as pd


def xlsx_to_csv_pd(input, output):
    data_xls = pd.read_excel(input, index_col=0)
    data_xls.to_csv(output, encoding='utf-8')


def csv_to_xlsx_pd(input, output):
    csv = pd.read_csv(input, encoding='utf-8')
    csv.to_excel(output, sheet_name='data')


