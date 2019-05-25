from typing import Mapping, Text

import faust


class RequestTransfer(faust.Record):
    src_account: str
    dst_account: str
    quantity: int


class BalanceUpdate(faust.Record):
    account: str
    quantity: int
    timestamp_committed: str


def balances_str(balances: Mapping[Text, int]) -> Text:
    return ', '.join(f'{k}: {balances[k]}' for k in sorted(balances.keys()))



DATETIME_BASIC_FORMAT = "%Y%m%dT%H%M%S"
