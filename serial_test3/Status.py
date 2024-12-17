# Status.py

from enum import Enum

class SerialPortStatus(Enum):
    OPEN  = True
    CLOSE = False

class OperationStatus(Enum):
    SUCCESS = True
    FAILURE = False

class ShutdownStatus(Enum):
    STARTUP  = True
    SHUTDOWN = False

class ResponseStatus(Enum):
    NOT_WAITING = True
    WAITING     = False
