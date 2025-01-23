# DEGITALINDICATOR/Indicator.py

import serial
import time
# 自作プログラムをimport
from SERIAL.manager.serial_communicator import SerialCommunicator
from DEGITALINDICATOR.Meas              import MeasurementConverter
from DEGITALINDICATOR.Compare           import Compare
from SERIAL.constant.Status             import OperationStatus

class Indicator:
    def __init__(self):
        serial_prams = {
        "port": "/dev/ttyUSB0",
        "baudrate": 2400,
        "parity": serial.PARITY_NONE,
        "stopbits": serial.STOPBITS_ONE,
        "timeout": 0.08,
        }
        self.serial_comm = SerialCommunicator(**serial_prams)        
        self.meas = MeasurementConverter()
        self.compare = Compare()
        time.sleep(3)

    def main(self, default_data: float) -> tuple[float, str]:
        self.serial_comm.serial_write(b's')
        result, status = self.serial_comm.serial_read_cr()
        if status == OperationStatus.FAILURE:
            return None
        data = self.meas.convertion_byte_float(result)
        # ここに判別処理を入れる
        judgment = self.compare.main(data, default_data)
        return data, judgment
        
