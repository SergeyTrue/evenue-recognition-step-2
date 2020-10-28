import attr
import pandas as pd


def _defer_or_recognize(instance, attrib, value):

    if value not in ['recognize', 'defer']:
        raise ValueError('action should be either recognize or defer')


@attr.s
class Shipment:
    data = attr.ib(type=pd.DataFrame)
    action = attr.ib(validator=_defer_or_recognize)



