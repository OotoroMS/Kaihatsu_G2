import time
import threading
import serial
from serial_communicator import SerialCommunicator

# シリアルポートの設定
PORT1 = "COM5"  # 適切なポートに変更してください
PORT2 = "COM3"  # 適切なポートに変更してください
BAUD_RATE = 9600
TIMEOUT = 0.1
PARITY = serial.PARITY_EVEN
STOPBITS = serial.STOPBITS_ONE

class SerialTest:
    def __init__(self):
        self.serial_comm1 = SerialCommunicator(PORT1, BAUD_RATE, PARITY, STOPBITS, TIMEOUT)
        self.serial_comm2 = SerialCommunicator(PORT2, BAUD_RATE, PARITY, STOPBITS, TIMEOUT)

    def send_test(self, append_newline=False):
        for i in range(5):
            data = f"Message {i}"
            if append_newline:
                data += "\r\n"  # 改行コードを追加
            data = data.encode()  # 送信するデータをバイト列に変換
            start_time = time.perf_counter()  # 経過時間の測定開始
            success = self.serial_comm1.write(data)  # データを送信
            elapsed_time = time.perf_counter() - start_time  # 経過時間の測定
            if success:
                print(f"Sent: {data} (Time taken: {elapsed_time:.6f} seconds)")
            else:
                print("Failed to send data.")

    def receive_test(self):
        for i in range(5):
            start_time = time.perf_counter()  # 経過時間の測定開始
            data = self.serial_comm2.read()  # データを受信
            elapsed_time = time.perf_counter() - start_time  # 経過時間の測定
            if data:
                print(f"Received: {data} (Time taken: {elapsed_time:.6f} seconds)")
            else:
                print(f"Failed to receive data(Time taken: {elapsed_time:.6f}.")

    def run_tests(self, send_only=False, receive_only=False, newline=False):
        if send_only:
            self.send_test(append_newline=newline)
        elif receive_only:
            self.receive_test()
        else:  # 送信と受信の両方を行う
            send_thread = threading.Thread(target=self.send_test, args=(newline,))
            receive_thread = threading.Thread(target=self.receive_test)

            send_thread.start()
            receive_thread.start()

            # スレッドの終了を待つ
            send_thread.join()
            receive_thread.join()

    def close_connections(self):
        self.serial_comm1.close()
        self.serial_comm2.close()

if __name__ == "__main__":
    test = SerialTest()
    
    # ユーザーにテストの種類を選ばせる
    print("Select the type of test:")
    print("1. Send only")
    print("2. Receive only")
    print("3. Send and receive")

    choice = input("Enter your choice (1/2/3): ")
    
    if choice == "1":
        newline_option = input("Send data with newline? (y/n): ")
        test.run_tests(send_only=True, newline=(newline_option.lower() == 'y'))
    elif choice == "2":
        test.run_tests(receive_only=True)
    elif choice == "3":
        newline_option = input("Send data with newline? (y/n): ")
        test.run_tests(newline=(newline_option.lower() == 'y'))
    else:
        print("Invalid choice. Please select 1, 2, or 3.")
    
    test.close_connections()  # 接続を閉じる
