# SerialUIBridge.py
# デバック用
import sys
import os
sys.path.append(os.getcwd())
import serial
from queue  import Queue
from typing import Optional, Tuple
from SERIAL.manager.plc_communicator import PLCCommunicator
from SERIAL.manager.dict_manager     import DictManager
from SERIAL.constant.Status  import OperationStatus

class SerialUIBridge(PLCCommunicator):
    def __init__(self, prams: dict):
        super().__init__(prams)
        self.queue = Queue()
        self.dict = DictManager()

    def read_loop(self):
        # データ受信        
        data, status = super().read()
        # 受信成功
        if status == OperationStatus.SUCCESS:
            # キューに値を入れる
            self.queue.put(data)
    
    # キューの中身があれば変換して取り出し
    def process_serial_queue(self):
        if self.queue.empty():
            return None, OperationStatus.FAILURE
        else:
            data = self.queue.get()
            # 辞書を使用して変換
            msg, status = self.dict.get_message(data)
            if status == OperationStatus.SUCCESS:
                return msg
            return None, status

if __name__ == '__main__':
    serial_params1 = {
        "port": "COM6",
        "baudrate": 9600,
        "parity": serial.PARITY_NONE,
        "stopbits": serial.STOPBITS_ONE,
        "timeout": 0.08,
    }
    test = SerialUIBridge(serial_params1)
    msg = test.process_serial_queue()
    print(msg)
    test.queue.put(b'\x02\x01')
    msg = test.process_serial_queue()
    print(msg)
    test.queue.put(b'\x01\xff')
    msg = test.process_serial_queue()
    print(msg)
            