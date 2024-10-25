import serial
import threading
from typing import Optional

class SerialCommunicator:
    def __init__(self, port: str, baudrate: int, parity: str, stopbits: int, timeout: Optional[float]):
        """
        初期化メソッド。シリアル通信の設定を行い、ロックオブジェクトを初期化する。

        引数:
            port (str): シリアルポートの名前
            baudrate (int): ボーレート（通信速度）
            parity (str): パリティ設定（例: 'N', 'E', 'O'）
            stopbits (int): ストップビットの設定
            timeout (Optional[float]): タイムアウトの設定（秒）
        """
        self.serial = serial.Serial(port, baudrate, bytesize=serial.EIGHTBITS,
                                    parity=parity, stopbits=stopbits, timeout=timeout)
        self.lock = threading.Lock()
        self.is_open: bool = True  # シリアル接続が開かれているかのフラグ

    def write(self, data: bytes) -> None:
        """
        シリアルポートにデータを送信する。スレッドセーフな操作のためにロックを使用。
        
        引数:
            data (bytes): 送信するデータ（バイト列）
        """
        with self.lock:
            try:
                self.serial.write(data)
                print(f"Data sent: {data}")
            except serial.SerialException as e:
                print(f"Error sending data via serial: {e}")

    def read(self) -> bytes:
        """
        シリアルポートからデータを受信する。スレッドセーフな操作のためにロックを使用。

        戻り値:
            bytes: 受信したデータ（バイト列）。エラーが発生した場合は空のバイト列を返す。
        """
        with self.lock:
            try:
                data = self.serial.readline()
                if data != b'':  # データが存在する場合のみ表示
                    print(f"Data received: {data}")
                return data
            except serial.SerialException as e:
                print(f"Error receiving data via serial port: {e}")
                return b''  # エラー発生時には空のバイト列を返す
    
    def close(self) -> None:
        """
        シリアルポートを閉じ、接続状態フラグを更新。
        """
        if self.serial.is_open:
            print(f"Closing serial port: {self.serial.name}")
            self.serial.close()
            self.is_open = False
