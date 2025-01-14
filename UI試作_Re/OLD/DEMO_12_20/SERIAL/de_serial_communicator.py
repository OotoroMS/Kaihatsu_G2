import serial
import threading
from time import perf_counter
from typing import Optional
import time

SERIALPORT_STATUS = {
    "serial_open": True,
    "serial_close": False
}
OPERATION_STATUS = {
    "success": True,
    "failure": False
}

ELAPSED_TIME = 0.0

# シリアル通信（接続・送信・受信・切断)を行うクラス
class SerialCommunicator:
    def __init__(self, port: str, baudrate: int, parity: str, stopbits: int, timeout: Optional[float]):
        self.serial = serial.Serial(
            port=port,
            baudrate=baudrate,
            bytesize=serial.EIGHTBITS,
            parity=parity,
            stopbits=stopbits,
            timeout=timeout
        )
        self.lock = threading.Lock() 
        self.is_open = SERIALPORT_STATUS["serial_open"]

    # データ送信関数。引数(byte型)を送信する。
    def serial_write(self, data: bytes) -> bool:        
        with self.lock:
            try:
                self.serial.write(data)
                return OPERATION_STATUS["success"]
            except serial.SerialException as e:
                print(f"Error sending data via serial:{e}")
                return OPERATION_STATUS["failure"]        

    # データ受信関数。受信したデータを返す。
    def serial_read(self) -> tuple[bytes, bool]:
        data = b''
        serial_none = 0
        with self.lock:
            try:
                # データが無しならとっとと次の処理に行く
                if self.serial.in_waiting > serial_none:
                    data = self.cr_readline()
                return data,OPERATION_STATUS["success"]
            except serial.SerialException as e:
                print(f"Error receiving data via serial port:{e}")
                return data,OPERATION_STATUS["failure"]
            
    # CRでreadを終了するやつ
    def cr_readline(self):
        # バッファを用意
        line = bytearray()
        while True:
            # 1バイトずつ読み込む
            char = self.serial.read()
            if not char:
                break   # ﾀｲﾑｱｳﾄの判定
            line.extend(char)   # バッファに追加
            if char == b'\r':    # CRが来た
                break
        return bytes(line)

    # 通信経路を切断する関数。終わるときに使用する。
    def serial_close(self) -> bool:
        if self.serial.is_open:
            try:
                print(f"Closing serial port: {self.serial.name}")
                self.serial.close()
                self.is_open = SERIALPORT_STATUS["serial_close"]
            except serial.SerialException as e:
                print(f"Error closing serial port: {e}")

    # テスト用メッセージ表示
    def log_message(self, msg: str):
        print(f"[TEST][Thread-{threading.get_ident()}] {msg}")        

    # テスト用メッセージ付き関数
    def log_serial_write(self, data: bytes):        
        # self.log_message("Lock serial_write")
        start_time = perf_counter()
        elapsed_time = ELAPSED_TIME
        self.serial_write(data)
        elapsed_time = perf_counter() - start_time
        self.log_message(f"Data sent: {data}(Time: {elapsed_time:.9f} sec)")        
        # self.log_message("Unlock serial_write")
    
    # テスト用メッセージ付き関数
    def log_serial_read(self):
        # self.log_message("Lock serial_read")
        start_time = perf_counter()  # 計測開始
        elapsed_time = ELAPSED_TIME
        test = self.serial_read()
        elapsed_time = perf_counter() - start_time  # 経過時間
        if test[0]:
            self.log_message(f"Data recv: {test[0]} (Time: {elapsed_time:.9f} sec)")  # 下1行も確認用
        return test
        # self.log_message("Unlock serial_read")

    # 外部から参照する用
    def send(self, data: bytes):
        # self.serial_write(data)
        self.log_serial_write(data)
    
    # 外部から参照する用
    def receive(self):
        # rcv_data = self.serial_read()
        rcv_data = self.log_serial_read()
        return rcv_data




