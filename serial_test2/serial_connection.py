import time
from queue import Queue
from serial_data_formatter import SerialDataFormatter
from serial_communicator import SerialCommunicator
from queue_manager import QueueManager

class SerialConnection:
    def __init__(self, port, baudrate, party, stopbits, timeout, snd_queue: Queue, rcv_queue: Queue):
        self.queue_manager = QueueManager(snd_queue, rcv_queue)
        self.data_formatter = SerialDataFormatter()
        self.serial_comm = SerialCommunicator(port, baudrate, party, stopbits, timeout)
        self.shutdown_flag = False
        self.wait_for_response = False

    def process_send_data(self):
        while not self.shutdown_flag:
            try:
                if self.serial_comm.is_open and not self.wait_for_response:
                    self.send_data_and_process()
                time.sleep(0.01)
            except Exception as e:
                print(f"Send unexpected error: {e}")

    def send_data_and_process(self):
        byte = self.queue_manager.send_queue_item()        
        if byte is not None:
            self.queue_manager.put_in_queue(self.queue_manager.send_queue, byte)
            data = self.data_formatter.format_send(byte)            
            self.serial_comm.write(data)
            self.wait_for_response = True

    def process_received_data(self):
        while not self.shutdown_flag:
            try:
                if self.serial_comm.is_open:
                    self.receive_data_and_process()
                time.sleep(0.01)
            except Exception as e:
                print(f"Receive unexpected error: {e}")

    def receive_data_and_process(self):
        data = self.serial_comm.read()        
        self.compare_recive_data(data)

    def compare_recive_data(self, data):
        if data.startswith(b'\x00\x01'):
            print("Received data")
            self.queue_manager.put_in_queue(self.queue_manager.receive_queue, data[2:3])
            self.send_response(data[2:3])
        elif data.startswith(b'\x00\x02'):
            print("Response data")
            self.compare_data(data)

    def send_response(self, response_data):
        response = b'\x00\x02' + response_data + b'\r\n'
        self.serial_comm.write(response)

    def compare_data(self, data):
        send_data = self.queue_manager.get_from_queue(self.queue_manager.send_queue)
        if data[2:3] == send_data:
            print("Data matches")
        else:
            print("Data does not match, resending")
            self.queue_manager.put_in_queue(self.queue_manager.send_queue, data)
        self.wait_for_response = False

    def close(self):
        if self.serial_comm and self.serial_comm.serial.is_open:
            print(f"Closing serial port: {self.serial_comm.serial.name}")
            self.serial_comm.serial.close()
            self.serial_comm.is_open = False

    def end(self):
        self.shutdown_flag = True
        self.close()
