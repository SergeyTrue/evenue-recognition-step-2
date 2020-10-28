from datetime import  datetime
import calendar
import pandas as pd

from rr_step_two.common.config import GL_ACCOUNTS, POSTING_KEYS, REGIONS
from rr_step_two.core.objects import Shipment


def create_single_upload_df(df, gl_accounts, posting_keys, period, cogs_or_ni, action):
    period = datetime.strptime(period, '%b %Y')
    last_day = datetime(period.year, period.month, calendar.monthrange(period.year, period.month)[-1])
    last_day = last_day.strftime('%d.%m.%Y')
    upload_df = create_empty_upload_df(df)
    upload_df.loc[0, 'Key(01)'] = 1
    upload_df.loc[1:, 'Key(01)'] = 2
    upload_df['Year(04)'] = period.year
    upload_df['Month(04)'] = period.month
    upload_df.loc[0, 'GL Account(10)'] = gl_accounts.loc[(cogs_or_ni, 'total')][0]
    upload_df.loc[1:, 'GL Account(10)'] = gl_accounts.loc[(cogs_or_ni, 'by_grosp')][0]
    upload_df[['Document Date(10)', 'Posting Date(10)']] = last_day
    if cogs_or_ni == 'cogs':
        upload_df['Amount(16)'] = df['cogs'].map('{:.2f}'.format).str.replace('.', ',')
    if cogs_or_ni == 'ni':
        upload_df['Amount(16)'] = df['ni'].map('{:.2f}'.format).str.replace('.', ',')
    upload_df['Text(40)'] = df['customer_name']
    upload_df.loc[0, 'Text(40)'] = df.loc[1, 'customer_name']
    upload_df['Company Code(04)'] = 'RU41'
    upload_df.loc[0, 'Posting Key(02)'] = posting_keys.loc[(cogs_or_ni, action, 'total')][0]
    upload_df.loc[1:, 'Posting Key(02)'] = posting_keys.loc[(cogs_or_ni, action, 'by_grosp')][0]
    upload_df.loc[0, 'customer_name'] = df.loc[1, 'customer_name']
    upload_df['Grospcode(04)'] = df['grosp']
    upload_df['Cost Center(10)'] = df['cost_center']
    upload_df.loc[0, 'Cost Center(10)'] = upload_df.loc[1, 'Cost Center(10)']
    upload_df['Currency(5)'] = 'RUB'
    upload_df['Taxcode(2)'] = 'BC'
    return upload_df


def make_gl_accounts_df():
    gl_accounts = pd.read_csv(GL_ACCOUNTS, sep=';')
    gl_accounts.columns = gl_accounts.columns.str.strip()
    gl_accounts = gl_accounts.applymap(lambda x: x.strip() if isinstance(x, str) else x)
    gl_accounts = gl_accounts.set_index(['ni_or_cogs', 'sum_type'])
    return gl_accounts


def create_empty_upload_df(df):
    columns = ['Key(01)', 'Year(04)', 'Month(04)', 'GL Account(10)', 'Document Date(10)', 'Posting Date(10)',
                'Amount(16)', 'Text(40)', 'Company Code(04)', 'Posting Key(02)', 'Customer Code(10)', 'Grospcode(04)',
                'Order Reason(3)', 'Cost Center(10)', 'Currency(5)', 'Taxcode(2)', 'Tax Jursdiction(15)',
                'Profit Center(10)', 'Order Number(12)', 'Plant(04)']
    df = pd.DataFrame('', index=range(0, len(df)), columns=columns)
    return df


def make_posting_keys_df():
    posting_keys = pd.read_csv(POSTING_KEYS, sep=';')
    posting_keys.columns = posting_keys.columns.str.strip()
    posting_keys = posting_keys.applymap(lambda x: x.strip() if isinstance(x, str) else x)
    posting_keys = posting_keys.set_index(['ni_or_cogs', 'action_type', 'sum_type'])
    return posting_keys


def add_empty_row(df):
    df1 = pd.DataFrame([[''] * len(df.columns)], columns=df.columns)
    df = df1.append(df, ignore_index=True)
    return df


def summarize_cogs_ni(df):
    df.loc[0, 'cogs'] = df.cogs[1:].sum()
    df.loc[0, 'ni'] = df.ni[1:].sum()
    return df


def process(report, history, last_run, period):
    gl_accounts = make_gl_accounts_df()
    posting_keys = make_posting_keys_df()
    regions_df = pd.read_excel(REGIONS)
    invoices_to_defer = report.loc[(report.action == 'отворачиваем') & (report.period == 'actual_period'), 'invoice']
    invoices_to_recognize = report.loc[(report.action == 'признаём') & (report.period == 'pending_to_recognize'),
                                       'invoice']
    lines_to_recognize = history[history.invoice.isin(invoices_to_recognize)]
    lines_to_defer = last_run[last_run.invoice.isin(invoices_to_defer)]

    grouped_lines_to_recognize = lines_to_recognize.groupby(['wbs_element'], as_index=False)
    grouped_lines_to_defer = lines_to_defer.groupby(['wbs_element'], as_index=False)
    dfs_by_wbs_to_recognize = [x for _, x in grouped_lines_to_recognize]
    dfs_by_wbs_to_defer = [x for _, x in grouped_lines_to_defer]
    shipments = []
    cogs_dfs, ni_dfs = [], []
    for item, _ in enumerate(dfs_by_wbs_to_recognize):
        shipment = Shipment(dfs_by_wbs_to_recognize[item], action='recognize')
        shipments.append(shipment)
    for item, _ in enumerate(dfs_by_wbs_to_defer):
        shipment = Shipment(dfs_by_wbs_to_defer[item], action='defer')
        shipments.append(shipment)
    for shipment in shipments:
        shipment.data = add_empty_row(shipment.data)
        shipment.data = shipment.data.merge(regions_df, on='fns', how='left')
        shipment.data = summarize_cogs_ni(shipment.data)
        cogs_df = create_single_upload_df(shipment.data, gl_accounts, posting_keys, period, 'cogs', shipment.action)
        cogs_dfs.append(cogs_df)
        ni_df = create_single_upload_df(shipment.data, gl_accounts, posting_keys, period, 'ni', shipment.action)
        ni_dfs.append(ni_df)

    cogs_upload_df = pd.concat(cogs_dfs)
    ni_upload_dfs = pd.concat(ni_dfs)
    return cogs_upload_df, ni_upload_dfs, invoices_to_defer, invoices_to_recognize
