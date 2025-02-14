# SERIAL/manager/serial_communcator.py

import serial
import logging
import threading
from time import perf_counter
from typing import Optional

# 自作プログラムをimport
# 型チェックのデコレータ, ログ作成
from UTILS.type_check import type_check_decorator
import UTILS.log_config as log
# 定数ファイル
from SERIAL.constant.Status     import OperationStatus

# シリアル通信（接続・送信・受信・切断)を行うクラス
class SerialCommunicator:
    def __init__(self, port: str, baudrate: int, parity: str, stopbits: int, timeout: float):
        self.serial = serial.Serial(
            port=port,
            baudrate=baudrate,
            bytesize=serial.EIGHTBITS,
            parity=parity,
            stopbits=stopbits,
            timeout=timeout
        )
        # ログを作成
        self.logger = log.setup_logging()
        self.logger.debug(f"シリアル通信開始：{self.serial.name}")
        self.lock: threading.Lock = threading.Lock()                

    # データ送信関数。引数(byte型)を送信する。
    @type_check_decorator({'data': bytes})
    def serial_write(self, data: bytes) -> OperationStatus:
        with self.lock:
            try:                
                self.serial.write(data)
                self.logger.debug(f"{self.serial.name} 送信：{data}")
                return OperationStatus.SUCCESS
            except serial.SerialException as e:
                self.logger.error(f"{self}: {self.serial_write.__name__}: {e}")
                return OperationStatus.FAILURE

    # データ受信関数。受信したデータを返す。
    def serial_read(self) -> tuple[bytes, OperationStatus]:
        data = b''
        serial_none = 0
        with self.lock:
            try:
                # データが無しならとっとと次の処理に行く
                if self.serial.in_waiting > serial_none:
                    data = self.serial.readline()
                    # print("serial_communicator.py serial_read : serial_read data is ", data)
                # 受信データの有無
                if data:
                    self.logger.debug(f"{self.serial.name} 受信：{data}")
                    return data, OperationStatus.SUCCESS
                # 無=失敗
                return data, OperationStatus.FAILURE
            except serial.SerialException as e:
                self.logger.error(f"{self}: {self.serial_read.__name__}: {e}")
                return data, OperationStatus.FAILURE
            
    # データ受信関数。CRを終端文字とする。
    def serial_read_cr(self) -> tuple[bytes, OperationStatus]:
        # バッファを用意
        line = bytearray()        
        with self.lock:
            try:
                while True:
                    # 1バイト分データを読み込む
                    char = self.read_char()
                    if char == b'': # タイムアウト発生
                        return bytes(line), OperationStatus.FAILURE                    
                    elif char:  # 配列に追加(データがある場合のみ)
                        self.logger.debug(f"一文字受信：{char}")
                        line.extend(char)
                    # CRかどうか判定 CRだったらTureが帰ってくる
                    if self.is_cr_terminated(char):
                        break
                self.logger.debug(f"{self.serial.name} 受信：{bytes(line)}")
                return bytes(line), OperationStatus.SUCCESS
            except serial.SerialException as e:
                self.logger.error(f"{self}: {self.serial_read_cr.__name__}: {e}")
                return bytes(line), OperationStatus.FAILURE

    # 1バイトを読み込む関数
    def read_char(self) -> bytes:        
        char = self.serial.read()
        return char

    # CRが終端文字かどうかを判定する関数
    def is_cr_terminated(self, char: bytes) -> bool:
        return char == b'\r'

    # 通信経路を切断する関数。終わるときに使用する。
    def serial_close(self) -> OperationStatus:
        if self.serial.is_open:
            try:                
                self.serial.close()
                self.logger.debug(f"シリアル通信終了：{self.serial.name}")
                return OperationStatus.SUCCESS
            except serial.SerialException as e:
                self.logger.error(f"{self}: {self.serial_close.__name__}: {e}")
                return OperationStatus.FAILURE

"""
    # テスト用メッセージ表示
    @type_check_decorator({'msg': str})
    def log_message(self, msg: str) -> None:
        print(f"[TEST][Thread-{threading.get_ident()}] {msg}")        

    # テスト用メッセージ付き関数
    @type_check_decorator({'data': bytes})
    def log_serial_write(self, data: bytes) -> OperationStatus:
        start_time = perf_counter()        
        status = self.serial_write(data)
        elapsed_time = perf_counter() - start_time
        self.log_message(f"Data sent: {data}(Time: {elapsed_time:.9f} sec)")
        return status
    
    # テスト用メッセージ付き関数
    def log_serial_read(self) -> tuple[bytes, OperationStatus]:        
        start_time = perf_counter()        
        byte, status = self.serial_read()
        elapsed_time = perf_counter() - start_time
        if byte:
            self.log_message(f"Data recv: {byte} (Time: {elapsed_time:.9f} sec)")  # 下1行も確認用
        return byte, status
"""

if __name__ == '__main__':
    pass