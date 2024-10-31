import threading
import serial
from serial_communicator import SerialCommunicator

# シリアルポートの設定
PORT1 = "COM5"  # 適切なポートに変更してください
PORT2 = "COM3"  # 適切なポートに変更してください
BAUD_RATE = 9600
TIMEOUT = 0.01
PARITY = serial.PARITY_EVEN
STOPBITS = serial.STOPBITS_ONE

SERIAL_STATUS = {
    "active": True,
    "inactive": False
}

LINEENDING = "\r\n"

# y/nのマッピング辞書
NEWLINE_OPTION = {
    'y': True,
    'n': False
}

class SerialTest:
    def __init__(self):
        self.serial_comm1 = SerialCommunicator(PORT1, BAUD_RATE, PARITY, STOPBITS, TIMEOUT)
        self.serial_comm2 = SerialCommunicator(PORT2, BAUD_RATE, PARITY, STOPBITS, TIMEOUT)

    def send_test(self, port, append_newline=NEWLINE_OPTION["n"]):
        for i in range(5):
            data = f"Message {i} from {SERIAL_PORTS[port]}".encode()  # 送信するデータをバイト列に変換
            if append_newline:
                data += LINEENDING.encode()  # 改行コードを追加

            port.serial_write(data)  # データを送信


    def receive_test(self, port):
        for i in range(5):
            port.serial_read()  # データを受信
            
    def run_tests(self, ports, operation, append_newline=NEWLINE_OPTION["n"]):
        threads = []
        
        for port in ports:
            if operation == "send" or operation == "both":
                send_thread = threading.Thread(target=self.send_test, args=(port, append_newline,))
                threads.append(send_thread)
                send_thread.start()
            if operation == "receive" or operation == "both":
                receive_thread = threading.Thread(target=self.receive_test, args=(port,))
                threads.append(receive_thread)
                receive_thread.start()

        # スレッドの終了を待つ
        for thread in threads:
            thread.join()

    def close_connections(self):
        print("Closing serial connections...")
        self.serial_comm1.serial_close()
        self.serial_comm2.serial_close()
        print("Serial connections closed.")

if __name__ == "__main__":
    test = SerialTest()

    SERIAL_PORTS = {
        test.serial_comm1: PORT1,
        test.serial_comm2: PORT2    
    }
    
    # ユーザーにテストの種類を選ばせる
    print("Select the type of operation:")
    print("1. Send only")
    print("2. Receive only")
    print("3. Send and receive")

    choice = input("Enter your choice (1/2/3): ")
    
    # 使用するポートの選択
    port_choice = input(f"Select the port (1 for {PORT1}, 2 for {PORT2}, 3 for both): ")

    if port_choice == "1":
        port = [test.serial_comm1]  # COM5
    elif port_choice == "2":
        port = [test.serial_comm2]  # COM3
    elif port_choice == "3":
        port = [test.serial_comm1, test.serial_comm2]  # 両方
    else:
        print("Invalid port choice. Please select 1, 2, or 3.")
        exit()

    if choice == "1":
        newline_option = input("Send data with newline? (y/n): ")
        append_newline = NEWLINE_OPTION.get(newline_option.lower(), False)  # 'y'または'n'を確認
        test.run_tests(port, "send", append_newline)  # 送信のみ
    elif choice == "2":
        test.run_tests(port, "receive")  # 受信のみ
    elif choice == "3":
        newline_option = input("Send data with newline? (y/n): ")
        append_newline = NEWLINE_OPTION.get(newline_option.lower(), False)  # 'y'または'n'を確認
        test.run_tests(port, "both", append_newline)  # 送受信両方
    else:
        print("Invalid choice. Please select 1, 2, or 3.")    
    
    test.close_connections()  # 接続を閉じる
