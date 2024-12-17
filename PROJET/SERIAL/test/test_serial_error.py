# SERIAL/test/test_serial_error.py
# デバック用
import sys
import os
sys.path.append(os.getcwd())

from SERIAL.manager.serial_communicator import SerialCommunicator
from SERIAL.constant.Status import OperationStatus
import time
import serial

# シリアルポートの設定
PORT1 = "COM3"  # 存在するポート
PORT2 = "COM9"  # 存在しないポート
BAUD_RATE = 9600
PARITY = serial.PARITY_EVEN
STOPBITS = serial.STOPBITS_ONE
TIMEOUT = 0.08

# 存在しないポート(これはログに出ない)
def test_invalid_port():
    try:
        SerialCommunicator(PORT2,BAUD_RATE,PARITY,STOPBITS,TIMEOUT)
    except Exception as e:
        print(f"存在しないポートテスト：エラー発生：{e}")
    
# 無効な型(これもログに出ない=こいつは出せるようにもできる)
def test_invalid_data_type():
    comm = SerialCommunicator(PORT1, BAUD_RATE, PARITY, STOPBITS, TIMEOUT)
    try:
        comm.serial_write("invalid data")   # 文字列を送ろうとしてみる
    except Exception as e:
        print(f"無効なデータ型テスト：エラー発生：{e}")

# タイムアウト(出ない)
def test_invalid_timeout():
    comm = SerialCommunicator(PORT1, BAUD_RATE, PARITY, STOPBITS, TIMEOUT)
    try:
        data, status = comm.serial_read_cr()    # データは来ない
        print(f"data = {data}, status = {status}")
    except Exception as e:
        print(f"タイムアウトエラー発生：{e}")

# 接続切断(出る)
def test_invalid_comm():
    comm = SerialCommunicator(PORT1, BAUD_RATE, PARITY, STOPBITS, TIMEOUT)
    try:
        comm.serial_write(b"test")
        input("ケーブルを抜いてください。")
        comm.serial_write(b"test")  # 再度送信を試みる
    except Exception as e:
        print(f"エラー発生: {e}")

if __name__ == "__main__":
    test_invalid_port()
    test_invalid_data_type()
    test_invalid_timeout()
    test_invalid_comm()
