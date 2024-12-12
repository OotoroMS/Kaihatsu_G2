# serial_communcator.py(プログラムファイル名+パス)
import serial
import threading
from time import perf_counter
from typing import Optional

# 自作プログラムをimport この３つはほかのプログラムでも使用している
# クラス名：関数名：エラー内容を引数に渡すことでエラー文をprintする関数
import log_error
# 引数の型をチェックするデコレータ
from type_check import type_check_decorator
# bool値をわかりやすい変数名にしたクラス 各状態フラグなどに使用する
from Status     import SerialPortStatus , OperationStatus

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
        self.lock: threading.Lock = threading.Lock()
        self.is_open: bool = SerialPortStatus.OPEN

    # データ送信関数。引数(byte型)を送信する。
    @type_check_decorator({'data': bytes})
    def serial_write(self, data: bytes) -> bool:        
        with self.lock:
            try:
                self.serial.write(data)
                return OperationStatus.SUCCESS
            except serial.SerialException as e:
                log_error(self, self.serial_write.__name__, e)
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
                return data, OperationStatus.SUCCESS
            except serial.SerialException as e:
                log_error(self, self.serial_read.__name__, e)
                return data, OperationStatus.FAILURE

    # 通信経路を切断する関数。終わるときに使用する。
    def serial_close(self) -> OperationStatus:
        if self.serial.is_open:
            try:
                print(f"Closing serial port: {self.serial.name}")
                self.serial.close()
                self.is_open = SerialPortStatus.CLOSE
                return OperationStatus.SUCCESS
            except serial.SerialException as e:
                log_error(self, self.serial_close.__name__, e)
                return OperationStatus.FAILURE

    # テスト用メッセージ表示
    @type_check_decorator({'msg': str})
    def log_message(self, msg: str) -> None:
        print(f"[TEST][Thread-{threading.get_ident()}] {msg}")        

    # テスト用メッセージ付き関数
    @type_check_decorator({'data': bytes})
    def log_serial_write(self, data: bytes) -> bool:
        start_time = perf_counter()        
        result = self.serial_write(data)
        elapsed_time = perf_counter() - start_time
        self.log_message(f"Data sent: {data}(Time: {elapsed_time:.9f} sec)")
        return result
    
    # テスト用メッセージ付き関数
    def log_serial_read(self) -> tuple[bytes, OperationStatus]:        
        start_time = perf_counter()        
        test = self.serial_read()
        elapsed_time = perf_counter() - start_time
        if test[0]:
            self.log_message(f"Data recv: {test[0]} (Time: {elapsed_time:.9f} sec)")  # 下1行も確認用
        return test        

