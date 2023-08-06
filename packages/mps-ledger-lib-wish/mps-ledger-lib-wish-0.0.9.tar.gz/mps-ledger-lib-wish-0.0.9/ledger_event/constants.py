from ledger_utils.py_enum import PyEnumMixin


class ServiceType(PyEnumMixin):
    ORDER = 1
    REFUND = 2
    POLICY = 3
    FINE = 4
    ONEOFF = 5


class LedgerEventType(PyEnumMixin):
    # MerchantTransaction related events.
    # - Logistics events
    ORDER_RELEASED = 1
    MARKED_SHIPPED = 2
    CONFIRMED_SHIPPED = 3
    CONFIRMED_DELIVERED = 4
    USER_CONFIRMED_DELIVERED = 5
    ARRIVE_AT_EPC_WAREHOUSE = 6
    REMOVED_FROM_A_PLUS = 7

    # - Refund events
    ORDER_REFUND = 200

    # - Policy events
    DISPUTE_SUCCESS = 300

    # Fine related items
    FINE_CREATION = 1000
    FINE_REVERSAL = 1001

    # Oneoff payment related items.
    ONEOFF_PAYMENT_CREATION = 2000
    ONEOFF_PAYMENT_CANCEL = 2001


SERVICE_TO_LEDGEREVENTS = {
    "ORDER": {
        LedgerEventType.ORDER_RELEASED,
        LedgerEventType.MARKED_SHIPPED,
        LedgerEventType.CONFIRMED_SHIPPED,
        LedgerEventType.CONFIRMED_DELIVERED,
        LedgerEventType.USER_CONFIRMED_DELIVERED,
        LedgerEventType.ARRIVE_AT_EPC_WAREHOUSE,
        LedgerEventType.REMOVED_FROM_A_PLUS,
    },
    "REFUND": {
        LedgerEventType.ORDER_REFUND,
    },
    "POLICY": {
        LedgerEventType.DISPUTE_SUCCESS,
    },
    "FINE": {
        LedgerEventType.FINE_CREATION,
        LedgerEventType.FINE_REVERSAL,
    },
    "ONEOFF": {
        LedgerEventType.ONEOFF_PAYMENT_CREATION,
        LedgerEventType.ONEOFF_PAYMENT_CANCEL,
    }
}
