import serial
import threading

class SerialCommunicator:
    def __init__(self, port, baudrate, party, stopbits, timeout):
        self.serial = serial.Serial(port, baudrate, bytesize=serial.EIGHTBITS,
                                    parity=party, stopbits=stopbits, timeout=timeout)
        self.lock = threading.Lock()
        self.is_open = True

    def write(self, data):
        with self.lock:
            try:
                self.serial.write(data)
                print(f"Data sent: {data}")
            except serial.SerialException as e:
                print(f"Error sending data via serial: {e}")

    def read(self):
        with self.lock:
            try:
                data = self.serial.readline()
                if data != b'':
                    print(f"Data received: {data}")
                return data
            except serial.SerialException as e:
                print(f"Error receiving data via serial port: {e}")
