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
from SERIAL.constant.Status  import OperationStatus, DictStatus

class SerialUIBridge(PLCCommunicator):
    def __init__(self, prams: dict):
        super().__init__(prams)
        self.rcv_queue = Queue()
        self.send_queue = Queue()
        self.dict = DictManager()

    def read_loop(self):
        # データ受信
        data, status = super().read()
        # 受信成功
        if status == OperationStatus.SUCCESS:
            # キューに値を入れる
            self.rcv_queue.put(data)
    
    # キューの中身があれば変換して取り出し
    def process_serial_queue(self):
        if self.rcv_queue.empty():
            return DictStatus.NONE.value, OperationStatus.FAILURE
        else:
            data = self.rcv_queue.get()
            # 辞書を使用して変換
            msg, status = self.dict.get_message(data)
            print(f"変換前:{data} 変換後:{msg}")
            return msg, status
    
    # データの送信用関数(キューに値があれば送信) これで使用するならこれをスレッド化すること!
    def send_loop(self):
        if self.send_queue.empty():
            return None
        else:
            data = self.send_queue.get()
            # キューのデータを送信データに変換
            super().send(data)

    # キューに値を入れる 
    def process_send_queue(self, data):
        self.send_queue.put(data)
    
    # データ送信
    def send_set(self, data):
        # 変換処理
        cmd,status = self.dict.str_to_byte(data)
        if status == OperationStatus.FAILURE:
            return None
        super().send(cmd)


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
    test.rcv_queue.put(b'\x02\x01')
    msg = test.process_serial_queue()
    print(msg)
    test.rcv_queue.put(b'\x01\xff')
    msg = test.process_serial_queue()
    print(msg)
            