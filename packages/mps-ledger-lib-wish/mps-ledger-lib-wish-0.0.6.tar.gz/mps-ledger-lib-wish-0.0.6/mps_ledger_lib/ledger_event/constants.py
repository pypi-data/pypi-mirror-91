from mps_ledger_lib.ledger_utils.py_enum import PyEnumMixin


class ServiceType(PyEnumMixin):
    ORDER = 1
    REFUND = 2
    POLICY = 3


class EventType(PyEnumMixin):
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


SERVICE_TO_EVENTS = {
    "ORDER": {
        EventType.ORDER_RELEASED,
        EventType.MARKED_SHIPPED,
        EventType.CONFIRMED_SHIPPED,
        EventType.CONFIRMED_DELIVERED,
        EventType.USER_CONFIRMED_DELIVERED,
        EventType.ARRIVE_AT_EPC_WAREHOUSE,
        EventType.REMOVED_FROM_A_PLUS,
    },
    "REFUND": {
        EventType.ORDER_REFUND,
    },
    "POLICY": {
        EventType.DISPUTE_SUCCESS,
    }
}
