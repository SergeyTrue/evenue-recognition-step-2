import argparse
import pathlib

from ._input_data import InputData
from ..common import HISTORY, LAST_RUN


def input_from_cmd() -> InputData:

    parser = argparse.ArgumentParser()
    parser.add_argument('--filled_report', type=str, required=True)
    parser.add_argument('--period', type=str, required=True)
    args = vars(parser.parse_args())
    filled_report = pathlib.Path(args['filled_report'])
    period = pathlib.Path(args['period'])

    input_ = InputData(filled_report=filled_report, history=HISTORY, last_run=LAST_RUN, period=period)

    return input_
