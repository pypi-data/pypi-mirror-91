from ledger_utils.py_enum import PyEnumMixin


class LedgerPayableType(PyEnumMixin):
    ORDER = 1
    FINE = 2
    ONEOFF = 3
