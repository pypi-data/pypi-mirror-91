import enum


@enum.unique
class HostType(enum.Enum):
    WORKER = 1
    COLLECTOR = 2
