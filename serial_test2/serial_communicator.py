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

WAIT_TIME = 0.01


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
        self.is_open = self.serialport_status("serial_open")

    def serial_write(self, data: bytes) -> bool:            
        print(f"[Thread-{threading.get_ident()}] Lock serial_write")
        start_time = perf_counter()  # 計測開始
        elapsed_time = 0.0
        with self.lock:
            try:
                self.serial.write(data)
                elapsed_time = perf_counter() - start_time  # 経過時間
                result = self.result("success")
            except serial.SerialException as e:
                print(f"[Thread-{threading.get_ident()}] Error sending data via serial: {e}")
                result = self.result("failure")
        print(f"[Thread-{threading.get_ident()}] Data sent: {data} (Time taken: {elapsed_time:.9f} seconds)")
        print(f"[Thread-{threading.get_ident()}] Unlock serial_write")
        self.wait_time()

        return result

    def serial_read(self) -> bytes:        
        print(f"[Thread-{threading.get_ident()}] Lock serial_read")
        start_time = perf_counter()  # 計測開始
        elapsed_time = 0.0        
        with self.lock:       
            try:
                if self.serial.in_waiting > 0:    # データが無しならとっとと次の処理に行く
                    data = self.serial.readline()
                    elapsed_time = perf_counter() - start_time  # 経過時間                                    
                else:
                    data = b''
                    elapsed_time = perf_counter() - start_time  # 経過時間                                    
                result = data
            except serial.SerialException as e:
                print(f"[Thread-{threading.get_ident()}] Error receiving data via serial port: {e}")
                result = b''                    
        print(f"[Thread-{threading.get_ident()}] Data received: {data} (Time taken: {elapsed_time:.9f} seconds)")
        print(f"[Thread-{threading.get_ident()}] Unlock serial_read")
        self.wait_time()

        return result

    def serial_close(self) -> bool:
        if self.serial.is_open:
            try:
                print(f"Closing serial port: {self.serial.name}")
                self.serial.close()
                self.is_open = self.serialport_status("serial_close")
                return self.result("success")
            except serial.SerialException as e:
                print(f"Error closing serial port: {e}")
                return self.result("failure")
        
    def wait_time(self):
        time.sleep(WAIT_TIME)

    def result(self, msg: str):
        result = OPERATION_STATUS[msg]
        return result
    
    def serialport_status(self, msg: str):
        result = SERIALPORT_STATUS[msg]
        return result

