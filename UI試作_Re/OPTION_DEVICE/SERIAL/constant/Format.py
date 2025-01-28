# SERIAL/constant/Format.py

from enum import Enum

class DataPrefix(Enum):
    ACK     = b'\x02'
    DATA_IN = b'\x01'
    NONE    = b''

class LineEnding(Enum):
    LF = b'\n'

class PLCDataPrefix(Enum):
    ACK     = b'\x02'
    DATA_IN = b'\x01'
    NONE    = b''
    NORMAL  = b'\x01'
    ERROR   = b'\x02' 