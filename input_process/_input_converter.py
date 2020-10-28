import pandas as pd
from openpyxl import load_workbook
from ._input_data import InputData


def get_data_from_input(input_data: InputData):
    filled_report_df = pd.read_excel(input_data.filled_report)
    history_df = pd.read_excel(input_data.history)
    last_run = pd.read_excel(input_data.last_run)
    with open(input_data.period, 'r') as stream:
        period = stream.read()

    return filled_report_df, history_df, last_run, period
