# SERIAL/test/test_plc.py

# デバック用
import sys
import os
sys.path.append(os.getcwd())

import serial
import struct
import threading

# 自作プログラムをimport
from SERIAL.manager.plc_Simulator import PLCSimulator


class Test:
    def __init__(self):
        serial_params1 = {
            "port": "COM3",
            "baudrate": 9600,
            "parity": serial.PARITY_NONE,
            "stopbits": serial.STOPBITS_ONE,
            "timeout": 0.08,
        }    
        self.plc_comm: PLCSimulator = PLCSimulator(serial_params1)
        self.inpt = None

    def main(self):
        while True:
            self.inpt = input("コマンドを入力してください(exitで抜ける):")
            if self.inpt == "exit":
                break
            try:
                # 入力を数値に変換
                number = int(self.inpt)
                # 数値をバイト列に変換（整数型として送信）
                data = struct.pack(">B", number)
                self.plc_comm.send(data)            
            except ValueError:
                print("Invalid input. Please enter a valid integer.")

    def read(self):
        while True:
            self.plc_comm.read()
            if self.inpt == exit:
                break

if __name__ == '__main__':
    test = Test()

    read = threading.Thread(target=test.read)
    read.daemon = True
    read.start()

    test.main()
