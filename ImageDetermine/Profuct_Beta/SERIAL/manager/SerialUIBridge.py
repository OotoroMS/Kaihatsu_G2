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
from SERIAL.constant.Work_status import *
import MEINTENANCE.CONSTANTS.move_moter_pos as MOVE_MOTOR_POS
import MEINTENANCE.CONSTANTS.operation_status as OPERATION_STATUS
class SerialUIBridge(PLCCommunicator):
    def __init__(self, prams: dict):
        super().__init__(prams)
        self.rcv_queue = Queue()
        self.send_queue = Queue()
        self.dict = DictManager()
        # ワーク状態
        self.in_work  = b'\xd0\n'
        self.out_work = b'\xce\n'
        self.move_pos = None
        self.operation_status = b'\xfd\n'

    def read_loop(self):
        # データ受信
        data, status = super().serial_read()
        # 受信成功
        if status == OperationStatus.SUCCESS:
            if data == IN_WORK_ON_STAUTS:
                self.in_work = data
            elif data == IN_WORK_OFF_STAUTS:
                self.in_work = data
            if data == OUT_WORK_ON_STAUTS:
                self.out_work = data
            elif data == OUT_WORK_OFF_STAUTS:
                self.out_work = data
            elif data in OPERATION_STATUS.OPERATION_ERROR_BYTES or data in OPERATION_STATUS.OPERATION_STOP_BYTES:
                self.operation_status = data
            elif data in MOVE_MOTOR_POS.MOTOR_POS_LIST:
                self.move_pos = data
            else:
                # キューに値を入れる
                self.rcv_queue.put(data)
                # print("SerialUIBridge.py read_loop data set")
            print("SerialUIBridge.py read_loop data is ", data)
    
    # キューの中身があれば変換して取り出し
    def process_serial_queue(self):
        if self.rcv_queue.empty():
            return None, OperationStatus.FAILURE
        else:
            data = self.rcv_queue.get()
            # print("SerialUIBridge.py process_serial_queue data is ", data)
            
            # 辞書を使用して変換
            msg, status = self.dict.get_message(data)
            if status == OperationStatus.SUCCESS:
                return msg
            return None, status
    
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
        cmd,status = self.dict.list_to_byte(data)
        if status == OperationStatus.FAILURE:
            return None
        # print("SerialUIBridge.py send_set cmd is ", cmd)
        super().send(cmd)
    
    def get_move_pos(self):
        move_pos = self.move_pos
        # self.move_pos = None
        return move_pos

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
            