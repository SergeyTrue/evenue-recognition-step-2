from pathlib import Path

HISTORY = r'C:\Users\belose\PycharmProjects\rr_1\rr_step_one\resources\history.xlsx'
LAST_RUN = r'C:\Users\belose\PycharmProjects\rr_1\rr_step_one\resources\last_run.xlsx'
PERIOD = r'C:\Users\belose\PycharmProjects\rr_1\rr_step_one\resources\period.txt'

RESOURCES = Path(__file__).parents[1] / 'resources'
GL_ACCOUNTS = RESOURCES / 'gl_accounts'
POSTING_KEYS = RESOURCES / 'posting_keys'
REGIONS = RESOURCES / 'regions.xlsx'
INVOICES_TO_RECOGNIZE = RESOURCES / 'invoices_to_recognize.txt'
INVOICES_TO_DEFER = RESOURCES / 'invoices_to_defer.txt'
