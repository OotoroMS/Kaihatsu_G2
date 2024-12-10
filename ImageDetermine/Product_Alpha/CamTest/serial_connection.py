import serial  # シリアル通信モジュールのインポート
import threading  # スレッドモジュールのインポート
import struct
import time

class SerialConnection:
    def __init__(self, port, baudrate=9600, timeout=1):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.send_word = b""
        self.receive_word = b""
        self.serial = None
        self.is_open = False
        self.lock = threading.Lock()
        self.shutdown_flag = False

    def connect(self):
        try:
            self.serial = serial.Serial(
                self.port, self.baudrate, bytesize=serial.EIGHTBITS, 
                parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, 
                timeout=self.timeout
            )
            self.is_open = True
        except serial.SerialException as e:
            raise ConnectionError(f"Failed to connect to serial port {self.port}: {e}")

    def set_send_word(self, word):
        with self.lock:
            if isinstance(word, str):
                self.send_word = word.encode('utf-8')
            elif isinstance(word, int):
                self.send_word = struct.pack('>B', word)
            elif isinstance(word, bytes):
                self.send_word = word
            else:
                raise ValueError("Unsupported data type for sending")

    def send_data(self):
        while not self.shutdown_flag:
            if self.is_open and self.send_word:
                with self.lock:
                    self.serial.write(self.send_word)
                    self.send_word = b""
            time.sleep(0.01)

    def get_receive_word(self):
        with self.lock:
            data = self.receive_word
            self.receive_word = b""
            return data

    def receive_data(self):
        while not self.shutdown_flag:
            if self.is_open:
                with self.lock:
                    data = self.serial.readline()
                    if data:
                        self.receive_word = data
            time.sleep(0.01)

    def close(self):
        if self.serial and self.serial.is_open:
            self.serial.close()
            self.is_open = False
        self.serial = None

    def start_communication(self):
        if self.is_open:
            self.receive_thread = threading.Thread(target=self.receive_data)
            self.receive_thread.start()

            self.send_thread = threading.Thread(target=self.send_data)
            self.send_thread.start()

    def stop_communication(self):
        self.shutdown_flag = True
        if hasattr(self, 'receive_thread'):
            self.receive_thread.join()
        if hasattr(self, 'send_thread'):
            self.send_thread.join()
        self.close()

# 利用例
if __name__ == "__main__":
    try:
        serial_conn = SerialConnection("COM3")
        serial_conn.connect()
        serial_conn.start_communication()

        # 送信データの設定と送信
        serial_conn.set_send_word(10)  # 例: 10という数値を送信
        time.sleep(1)  # 送信の待機時間

        # 受信データの取得
        received_data = serial_conn.get_receive_word()
        if received_data:
            print(f"Received data: {received_data}")

    except KeyboardInterrupt:
        print("Program interrupted.")
    finally:
        serial_conn.stop_communication()
        print("Program terminated.")
