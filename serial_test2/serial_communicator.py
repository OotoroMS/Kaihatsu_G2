import serial
import threading
from typing import Optional

SERIALPORT_STATUS = {
    "serial_open": True,
    "serial_close": False
}

OPERATION_STATUS = {
    "success": True,
    "failure": False
}


class SerialCommunicator:
    def __init__(self, port: str, baudrate: int, parity: str, stopbits: int, timeout: Optional[float]):
        """
        シリアル通信の設定を初期化し、スレッドロックをセットアップ。
        """
        self.serial = serial.Serial(
            port=port,
            baudrate=baudrate,
            bytesize=serial.EIGHTBITS,
            parity=parity,
            stopbits=stopbits,
            timeout=timeout
        )
        self.lock = threading.Lock()
        self.is_open: bool = SERIALPORT_STATUS["serial_open"]

    def serial_write(self, data: bytes) -> bool:
        """
        シリアルポートにデータを送信。スレッドセーフな操作のためロックを使用。
        
        引数:
            data (bytes): 送信するデータ（バイト列）
        
        戻り値:
            bool: 送信が成功したかどうか
        """
        with self.lock:
            # スレッドロックが正常にかかっているか確認する  実稼働の時はコメントアウトさせておくこと
            print(f"[Thread-{threading.get_ident()}] Lock serial_write")
            try:
                self.serial.write(data)
                print(f"[Thread-{threading.get_ident()}] Data sent: {data}")
                return OPERATION_STATUS["success"]
            except serial.SerialException as e:
                print(f"[Thread-{threading.get_ident()}] Error sending data via serial: {e}")
                return OPERATION_STATUS["failure"]
            # スレッドロックが正常にかかっているか確認する  実稼働の時はコメントアウトさせておくこと(finallyごと)
            finally:
                print(f"[Thread-{threading.get_ident()}] Unlock serial_write")

    def serial_read(self) -> bytes:
        """
        シリアルポートからデータを受信。スレッドセーフな操作のためロックを使用。
        
        戻り値:
            bytes: 受信したデータ（バイト列）、エラー時は空のバイト列を返す
        """
        with self.lock:
            # スレッドロックが正常にかかっているか確認する  実稼働の時はコメントアウトさせておくこと
            print(f"[Thread-{threading.get_ident()}] Lock serial_read")
            try:
                data = self.serial.readline()
                if data:
                    print(f"[Thread-{threading.get_ident()}] Data received: {data}")
                return data
            except serial.SerialException as e:
                print(f"[Thread-{threading.get_ident()}] Error receiving data via serial port: {e}")
                return b''
            # スレッドロックが正常にかかっているか確認する  実稼働の時はコメントアウトさせておくこと(finallyごと)
            finally:
                print(f"[Thread-{threading.get_ident()}] Unlock serial_read")

    def serial_close(self) -> bool:
        """
        シリアルポートを閉じ、接続状態を更新。
        
        戻り値:
            bool: シリアルポートが正常に閉じられたかどうか
        """
        if self.serial.is_open:
            try:
                print(f"Closing serial port: {self.serial.name}")
                self.serial.close()
                self.is_open = SERIALPORT_STATUS["serial_close"]
                return OPERATION_STATUS["success"]
            except serial.SerialException as e:
                print(f"Error closing serial port: {e}")
                return OPERATION_STATUS["failure"]
