# SERIAL/test/test_serial_receive.py
# デバック用
import sys
import os
sys.path.append(os.getcwd())

from SERIAL.manager.serial_communicator import SerialCommunicator
from SERIAL.constant.Status import OperationStatus
import time
import serial

# シリアルポートの設定
PORT1 = "COM4"  # 適切なポートに変更してください
BAUD_RATE1 = 9600
BAUD_RATE2 = 2400
PARITY1 = serial.PARITY_EVEN
PARITY2 = serial.PARITY_NONE
STOPBITS = serial.STOPBITS_ONE
TIMEOUT = 0.08

def test_serial_receive():
    serial_comm = SerialCommunicator(PORT1, BAUD_RATE1, PARITY1, STOPBITS, TIMEOUT)

    while True:
        data, status = serial_comm.serial_read()
        
        if status == OperationStatus.SUCCESS:
            print(f"受信データ: {data.decode('utf-8')}")
            if data.decode('utf-8') == "END":
                print("終了コマンドを受信しました。通信を終了します。")
                break
        else:
            pass            
    
    serial_comm.serial_close()


def test_serial_receive_cr():
    serial_comm = SerialCommunicator(PORT1, BAUD_RATE2, PARITY2, STOPBITS, TIMEOUT)

    while True:
        data, status = serial_comm.serial_read_cr()
        
        if status == OperationStatus.SUCCESS:
            print(f"受信データ: {data.decode('utf-8')}")
            if data.decode('utf-8').strip() == "END":
                print("終了コマンドを受信しました。通信を終了します。")
                break
        else:
            pass         
    
    serial_comm.serial_close()

# テストの実行
if __name__ == "__main__":
    test_serial_receive()
