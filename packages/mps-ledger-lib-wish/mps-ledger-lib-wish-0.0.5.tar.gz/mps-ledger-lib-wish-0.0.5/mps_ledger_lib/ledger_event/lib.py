from mps_ledger_lib.ledger_utils.py_enum import PyEnumMixin


class ServiceType(PyEnumMixin):
    ORDER = 1


class EventType(PyEnumMixin):
    ORDER_RELEASED = 1


SERVICE_TO_EVENTS = {
    "ORDER": {
        EventType.ORDER_RELEASED
    },
}
