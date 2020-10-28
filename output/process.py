import os

import tempfile
from datetime import datetime
import time
import subprocess


def save_dfs(cogs_df, ni_df, period):
    os.chdir(tempfile.gettempdir())
    temporary_dir = os.getcwd()
    folder_name = time.strftime('%Y-%m-%d_%H-%M-%S') + '_revenue_recognition'
    os.mkdir(os.path.join(temporary_dir, folder_name))
    full_folder_path = os.path.join(temporary_dir, folder_name)
    period = datetime.strptime(period, '%b %Y')
    month = period.strftime('%b').upper()
    year = period.strftime('%Y')
    ni_filename = f'zfiupload template f-02_RU41_RR_NI_{month}_{year}.xlsx'
    cogs_filename = f'zfiupload template f-02_RU41_RR_COS_{month}_{year}.xlsx'
    full_cogs_path = os.path.join(full_folder_path, cogs_filename)
    full_ni_path = os.path.join(full_folder_path, ni_filename)
    cogs_df.to_excel(full_cogs_path, index=False, engine='openpyxl')
    ni_df.to_excel(full_ni_path, index=False, engine='openpyxl')
    file_browser_path = os.path.join(os.getenv('WINDIR'), 'explorer.exe')
    subprocess.run([file_browser_path, folder_name])

def save_invoices(invoices_to_defer, invoices_to_recognize):
    pass

