from .input_process import input_from_cmd, get_data_from_input
from .processor import process
from .output import save_dfs
from .common.config import INVOICES_TO_DEFER, INVOICES_TO_RECOGNIZE


input_data = input_from_cmd()
filled_report_df, history_df, last_run, period = get_data_from_input(input_data)
cogs_upload_df, ni_upload_dfs, invoices_to_defer, invoices_to_recognize = \
    process(filled_report_df, history_df, last_run, period)
save_dfs(cogs_upload_df, ni_upload_dfs, period)
invoices_to_recognize.to_csv(INVOICES_TO_RECOGNIZE, index=False, header=False)
invoices_to_defer.to_csv(INVOICES_TO_DEFER, index=False, header=False)
