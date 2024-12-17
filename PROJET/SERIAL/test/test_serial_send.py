# SERIAL/test/test_serial_send.py
# デバック用
import sys
import os
sys.path.append(os.getcwd())

from SERIAL.manager.serial_communicator import SerialCommunicator
from SERIAL.constant.Status import OperationStatus
import time
import serial

# シリアルポートの設定
PORT1 = "COM3"  # 適切なポートに変更してください
BAUD_RATE1 = 9600
BAUD_RATE2 = 2400
PARITY1 = serial.PARITY_EVEN
PARITY2 = serial.PARITY_NONE
STOPBITS = serial.STOPBITS_ONE
TIMEOUT = 0.08

def test_serial_send():
    serial_comm = SerialCommunicator(PORT1, BAUD_RATE1, PARITY1, STOPBITS, TIMEOUT)
    
    while True:
        user_input = input("送信するデータを入力してください（終了は'END'）：")        
        
        data = user_input.encode('utf-8')
        status = serial_comm.serial_write(data)        
        
        if status == OperationStatus.SUCCESS:
            print(f"送信成功: {user_input}")
        else:
            print("送信に失敗しました。")
            
        if user_input == "END":
            print("終了します。")
            break
        
    serial_comm.serial_close()

def test_serial_send_cr():
    serial_comm = SerialCommunicator(PORT1, BAUD_RATE2, PARITY2, STOPBITS, TIMEOUT)
    
    while True:
        user_input = input("送信するデータを入力してください（終了は'END'）：")        
        
        data = user_input.encode('utf-8') + b"\r"
        status = serial_comm.serial_write(data)        
        
        if status == OperationStatus.SUCCESS:
            print(f"送信成功: {user_input}")
        else:
            print("送信に失敗しました。")
            
        if user_input == "END":
            print("終了します。")
            break
        
    serial_comm.serial_close()

# テストの実行
if __name__ == "__main__":
    test_serial_send()  # 送信ポートを指定
