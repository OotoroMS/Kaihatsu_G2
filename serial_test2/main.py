from serial_connection import SerialConnection
from process_queue import QueueCreate
import threading
import serial

# シリアルポートの設定
PORT1 = "COM5"
BAUD_RATE = 9600
TIMEOUT = 0.05
PARTY = serial.PARITY_EVEN
STOPBITS = serial.STOPBITS_ONE

# グローバル変数
command = None
command_flag = False

class Instance:
    def __init__(self, params):
        # 各要素のインスタンス化
        queue_creator = QueueCreate()
        self.queues = queue_creator.get_communication_queues()
        self.serial_conn = SerialConnection(params, self.queues)

    def main(self):
        # メイン処理        
        self.thread_start()
        self.run_main_loop()

    def thread_start(self):
        # スレッドの作成と開始
        if self.serial_conn.serial_comm.is_open:            
            self.send_th = threading.Thread(target=self.serial_conn.process_received_data, daemon=True)
            self.send_th.start()

            self.rcv_th = threading.Thread(target=self.serial_conn.process_send_data, daemon=True)
            self.rcv_th.start()        
        self.cma_th = threading.Thread(target=input_thread, daemon=True)
        self.cma_th.start()

    def run_main_loop(self):
        global command
        snd_queue = self.queues['send_queue']
        rcv_queue = self.queues['receive_queue']
        
        while True:
            if command == "exit":
                break

            if command:
                snd_queue.put(command)
                command = None

            if not rcv_queue.empty():
                data = rcv_queue.get()
                if data != b'':
                    print(f"これが外部に渡すやつ: {data}")

    def thread_stop(self):
        global command_flag
        self.serial_conn.end()    
        command_flag = True

        # スレッドを終了させる
        self.send_th.join()
        self.rcv_th.join()
        self.cma_th.join()


def input_thread():    
    global command
    while not command_flag:
        command = input("コマンドを入力してください (exitで終了): ")
        if command == "exit":
            break

def main():    
    global command, command_flag
    try:
        serial_params = {
            "port": PORT1,
            "baudrate": BAUD_RATE,
            "party": PARTY,
            "stopbits": STOPBITS,
            "timeout": TIMEOUT,         
        }

        test = Instance(serial_params)
        test.main()

    except KeyboardInterrupt:
        print("プログラムが中断されました.")
    finally:
        pass

if __name__ == "__main__":
    main()
