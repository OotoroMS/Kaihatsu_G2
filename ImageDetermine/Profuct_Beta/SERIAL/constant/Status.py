# SERIAL/constant/Status.py

from enum import Enum

class OperationStatus(Enum):
    SUCCESS = True
    FAILURE = False

class DictStatus(Enum):
    NONE = [None, None]

class ShutdownStatus(Enum):
    STARTUP  = True
    SHUTDOWN = False

class ResponseStatus(Enum):
    NOT_WAITING = True
    WAITING     = False

class DataPrefix(Enum):
    ACK = b'\x02'
    DATA_IN = b'\x01'

class LineEnding(Enum):
    LINE_END = b'\n'