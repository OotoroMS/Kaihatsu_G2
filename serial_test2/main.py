import threading
import serial
from serial_manager import SerialManager
from queue_create import QueueCreate
from typing import Dict, Any, Optional

# シリアルポートの設定
PORT1: str = "COM5"
BAUD_RATE: int = 9600
TIMEOUT: float = 0.05
PARITY: int = serial.PARITY_EVEN
STOPBITS: int = serial.STOPBITS_ONE

class Instance:
    def __init__(self, params: Dict[str, Any]):
        self.command: Optional[str] = None
        self.command_flag: bool = False

        # 各要素のインスタンス化
        queue_creator = QueueCreate()
        self.queues = queue_creator.get_communication_queues()
        self.serial_conn = SerialManager(params, self.queues)

    def main(self) -> None:
        self.thread_start()  # スレッドを開始
        self.run_main_loop()  # メインループを実行
        self.thread_stop()  # スレッドを停止

    def thread_start(self) -> None:
        if self.serial_conn.serial_comm.is_open:
            self.send_th = threading.Thread(target=self.serial_conn.process_received_data, daemon=True)
            self.send_th.start()
            self.rcv_th = threading.Thread(target=self.serial_conn.process_send_data, daemon=True)
            self.rcv_th.start()
            self.cma_th = threading.Thread(target=self.input_thread, daemon=True)
            self.cma_th.start()

    def run_main_loop(self) -> None:
        snd_queue = self.queues['send_queue']
        rcv_queue = self.queues['receive_queue']
        
        while True:
            if self.command == "exit":
                break

            if self.command:
                snd_queue.put(self.command)
                self.command = None

            if not rcv_queue.empty():
                data = rcv_queue.get()
                if data != b'':
                    print(f"これが外部に渡すやつ: {data}")

    def thread_stop(self) -> None:
        self.command_flag = True
        self.serial_conn.end()
        self.send_th.join()
        self.rcv_th.join()
        self.cma_th.join()

    def input_thread(self) -> None:
        while not self.command_flag:
            self.command = input("コマンドを入力してください (exitで終了): ")
            if self.command == "exit":
                break

def main() -> None:    
    try:
        serial_params = {
            "port": PORT1,
            "baudrate": BAUD_RATE,
            "parity": PARITY,
            "stopbits": STOPBITS,
            "timeout": TIMEOUT,
        }

        test = Instance(serial_params)
        test.main()

    except KeyboardInterrupt:
        print("プログラムが中断されました.")
    finally:
        # ここでスレッドを停止させることができます
        pass

if __name__ == "__main__":
    main() 
