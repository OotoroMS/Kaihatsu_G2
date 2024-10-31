import serial
import threading
from time import perf_counter
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
        print(f"[Thread-{threading.get_ident()}] Lock serial_write")
        start_time = perf_counter()  # 計測開始
        elapsed_time = 0.0
        with self.lock:
            try:
                self.serial.write(data)
                elapsed_time = perf_counter() - start_time  # 経過時間
                result = OPERATION_STATUS["success"]
            except serial.SerialException as e:
                print(f"[Thread-{threading.get_ident()}] Error sending data via serial: {e}")
                result =  OPERATION_STATUS["failure"]
        print(f"[Thread-{threading.get_ident()}] Data sent: {data} (Time taken: {elapsed_time:.9f} seconds)")
        print(f"[Thread-{threading.get_ident()}] Unlock serial_write")

        return result

    def serial_read(self) -> bytes:        
        print(f"[Thread-{threading.get_ident()}] Lock serial_read")
        start_time = perf_counter()  # 計測開始
        elapsed_time = 0.0
        with self.lock:       
            try:
                data = self.serial.readline()
                elapsed_time = perf_counter() - start_time  # 経過時間                
                result = data
            except serial.SerialException as e:
                print(f"[Thread-{threading.get_ident()}] Error receiving data via serial port: {e}")
                result = b''            
        if data:
            print(f"[Thread-{threading.get_ident()}] Data received: {data} (Time taken: {elapsed_time:.9f} seconds)")
        print(f"[Thread-{threading.get_ident()}] Unlock serial_read")

        return result

    def serial_close(self) -> bool:
        if self.serial.is_open:
            try:
                print(f"Closing serial port: {self.serial.name}")
                self.serial.close()
                self.is_open = SERIALPORT_STATUS["serial_close"]
                return OPERATION_STATUS["success"]
            except serial.SerialException as e:
                print(f"Error closing serial port: {e}")
                return OPERATION_STATUS["failure"]
