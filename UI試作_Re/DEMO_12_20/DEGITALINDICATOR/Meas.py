from DEGITALINDICATOR.ConvertionByteFloat import *
from SERIAL.de_serial_communicator import SerialCommunicator
from SERIAL.pc_comands import PCManager
import serial
import time

# シリアルポートの設定
PORT1 = "COM3"  # 適切なポートに変更してください
BAUD_RATE = 2400
TIMEOUT = 0.08
PARITY = serial.PARITY_NONE
STOPBITS = serial.STOPBITS_ONE
LINEENDING = b"\n"
DATA_PREFIX = b"\x01"

serial_params1 = {
    "port": PORT1,
    "baudrate": BAUD_RATE,
    "parity": PARITY,
    "stopbits": STOPBITS,
    "timeout": TIMEOUT
}

class Meas:
    def __init__(self, serial_params: dict):
        # シリアル通信
        self.serial: SerialCommunicator = SerialCommunicator(**serial_params)
        self.manager: PCManager = PCManager(self.serial)

    def meas_read(self):
        while True:
            text = self.manager.read()
            return text
        
    def meas_get(self, text):
        result = None
        if text[0] == '正常001':
            self.serial.log_serial_write(b's')
            while True:
                data = self.serial.log_serial_read()                 
                if data[0]:                    
                    result = convertion_byte_froat(data[0])
                    return result
                # test_data = b'01A+000.1111\r'
                # result = convertion_byte_froat(test_data)
        else:
            print("送信命令ではありません")
            return None
    
    def meas(self):
        text = self.meas_read()
        result = self.meas_get(text)
        if result:
            print(result)
            return result
        return None

if __name__ == "__main__":
    # byte = {
    #     b'01A+000.0101\r',
    #     b'01A+11111111\r',
    #     b'01A+000.1111\r',
    #     b'01A+111.0000\r',
    #     b'01A+000.0000\r',
    #     b'911\r',
    #     b'912\r'
    # }
    # for i in byte:        
    #     result = convertion_byte_froat(i)
    #     print("bytes :",str(i)," result:", result)

    data = ["正常001", "投入部"]
    print(data[0])
    test = Meas(serial_params1)
    time.sleep(3)
    result = test.meas_get(data)
    print(f"{result}のずれ")
    test.serial.serial_close()    