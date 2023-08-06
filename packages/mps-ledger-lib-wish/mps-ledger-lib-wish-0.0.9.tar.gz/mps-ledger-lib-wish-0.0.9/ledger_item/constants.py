from ledger_utils.py_enum import PyEnumMixin


class LedgerItemState(PyEnumMixin):
    NEW = 1
    SETTLED = 2


class LedgerItemType(PyEnumMixin):
    # MerchantTransaction related items.
    ORDER = 1
    REFUND = 2

    # Fine related items
    DEDUCTION = 100
    REVERSAL = 101

    # Oneoff payment related items.
    ONEOFF_PAYMENT = 200
    ONEOFF_PAYMENT_CANCELLATION = 201

    # Merchant payment related items
    PAYMENT = 1000


class PaymentType(PyEnumMixin):
    CREDIT = 1
    DEBIT = 2
