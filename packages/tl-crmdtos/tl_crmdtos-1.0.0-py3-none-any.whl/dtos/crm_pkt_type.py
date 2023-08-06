import enum


@enum.unique
class CrmPktType(enum.Enum):
    PROBE_INIT = 1
    PROBE_ACK = 2
    REG_ACK = 3
