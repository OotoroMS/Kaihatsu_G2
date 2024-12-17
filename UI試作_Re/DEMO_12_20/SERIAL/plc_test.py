import threading
import serial
import struct
from SERIAL.serial_communicator import SerialCommunicator
from SERIAL.plc_pc import SerialManager
from SERIAL.pc_comands import PCManager

# シリアルポートの設定
PORT1 = "COM3"  # 適切なポートに変更してください
BAUD_RATE = 9600
TIMEOUT = 0.08
PARITY = serial.PARITY_EVEN
STOPBITS = serial.STOPBITS_ONE
LINEENDING = b"\n"
DATA_PREFIX = b"\x01"

serial_params1 = {
    "port": PORT1,
    "baudrate": BAUD_RATE,
    "parity": PARITY,
    "stopbits": STOPBITS,
    "timeout": TIMEOUT,
}


class SerialTest:
    def __init__(self):
        self.serial_comm1 = SerialManager(serial_params1)
        self.serial_test = PCManager(self.serial_comm1)
        self.user_input = ""

    def send_input_test(self):
        """キーボード入力から数値を取得し、シリアルポートに送信"""
        while True:
            self.user_input = input("Enter a number to send (type 'exit' to quit): ")
            if self.user_input.lower() == "exit":
                break
            try:
                # 入力を数値に変換
                number = int(self.user_input)
                # 数値をバイト列に変換（整数型として送信）
                data = struct.pack(">B", number)
                self.serial_test.write_serial(data)
            except ValueError:
                print("Invalid input. Please enter a valid integer.")

    def receive_until_command(self):
        """データを受信し続け、'exit' コマンドが受信されると停止"""
        while True:
            self.serial_test.read()
            if self.user_input.lower() == "exit":
                break

    def run_tests(self):
        """テストの種類を選択して実行"""
        print("Select the operation mode:")
        print("1. Send numbers from keyboard")
        print("2. Receive until 'exit' command")
        print("3. Send and receive simultaneously")

        choice = input("Enter your choice (1/2/3): ")

        if choice == "1":
            self.send_input_test()
        elif choice == "2":
            self.receive_until_command()
        elif choice == "3":
            # 送信と受信を同時に行うためにスレッドを作成
            send_thread = threading.Thread(target=self.send_input_test)
            receive_thread = threading.Thread(target=self.receive_until_command)

            # スレッドの開始
            send_thread.start()
            receive_thread.start()

            # 両方のスレッドの終了を待機
            send_thread.join()
            receive_thread.join()
        else:
            print("Invalid choice. Please select 1, 2, or 3.")

    def close_connection(self):
        """シリアル接続を閉じる"""
        print("Closing serial connection...")
        self.serial_comm1.serial_close()
        print("Serial connection closed.")

def main():
    test = SerialTest()
    
    try:
        test.run_tests()
    finally:
        test.close_connection()

if __name__ == "__main__":
    main()
