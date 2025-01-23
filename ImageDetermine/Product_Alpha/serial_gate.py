# シリアル通信の窓口プログラム

import serial
import time
import serial_communicator as PLC_Lib
import threading


class SerialGate:
    # コンストラクタ
    def __init__(self, serial_params, stop_event: threading.Event):
        # シリアル通信のパラメータ
        self.serial_params = serial_params
        self.stop_event = stop_event
        self.r_data = b''
        # シリアル通信のインスタンスを生成
        serial_comm = PLC_Lib.SerialCommunicator(**self.serial_params)

    # 受信ループ (スレッド化して呼び出す)
    def receive_loop(self):
        # 無限ループ
        while not self.stop_event.is_set():
            # 受信
            rcv_data, flag = self.serial_comm.serial_read()
            self.r_data = rcv_data
            time.sleep(0.1)

    def get_receive_data(self):
        return self.r_data
    
    # 送信
    def send(self, data: bytes):
        # 送信
        self.serial_comm.serial_write(data)
        time.sleep(0.1)