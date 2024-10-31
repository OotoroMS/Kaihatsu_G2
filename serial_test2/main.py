import threading
import serial
from serial_test2.serial_manager import SerialManager
from serial_test2.queue_create import QueueCreate
from typing import Dict, Any, Optional

# シリアルポートの設定
PORT1: str = "COM5"
BAUD_RATE: int = 9600
TIMEOUT: float = 0.05
PARTY: int = serial.PARITY_EVEN
STOPBITS: int = serial.STOPBITS_ONE

# グローバル変数
command: Optional[str] = None
command_flag: bool = False

class Instance:
    def __init__(self, params: Dict[str, Any]):
        """
        Instanceクラスのコンストラクタ。

        引数:
            params (Dict[str, Any]): シリアル通信の設定パラメータ
        """
        # 各要素のインスタンス化
        queue_creator = QueueCreate()
        self.queues = queue_creator.get_communication_queues()
        self.serial_conn = SerialManager(params, self.queues)

    def main(self) -> None:
        """
        メイン処理を開始する。
        """
        self.thread_start()  # スレッドを開始
        self.run_main_loop()  # メインループを実行

    def thread_start(self) -> None:
        """
        スレッドの作成と開始を行う。
        """
        if self.serial_conn.serial_comm.is_open:
            # 受信データを処理するスレッドの作成
            self.send_th = threading.Thread(target=self.serial_conn.process_received_data, daemon=True)
            self.send_th.start()

            # 送信データを処理するスレッドの作成
            self.rcv_th = threading.Thread(target=self.serial_conn.process_send_data, daemon=True)
            self.rcv_th.start()

        # コマンド入力用のスレッドの作成
        self.cma_th = threading.Thread(target=input_thread, daemon=True)
        self.cma_th.start()

    def run_main_loop(self) -> None:
        """
        メインループを実行し、コマンドの入力とキューからのデータ処理を行う。
        """
        global command
        snd_queue = self.queues['send_queue']
        rcv_queue = self.queues['receive_queue']
        
        while True:
            if command == "exit":
                break  # "exit" コマンドでループを終了

            if command:
                snd_queue.put(command)  # コマンドを送信キューに追加
                command = None

            if not rcv_queue.empty():
                data = rcv_queue.get()  # 受信キューからデータを取得
                if data != b'':
                    print(f"これが外部に渡すやつ: {data}")

    def thread_stop(self) -> None:
        """
        スレッドを停止させ、接続を終了する。
        """
        global command_flag
        self.serial_conn.end()    
        command_flag = True

        # スレッドを終了させる
        self.send_th.join()
        self.rcv_th.join()
        self.cma_th.join()


def input_thread() -> None:    
    """
    コマンド入力用のスレッドを実行する関数。
    """
    global command
    while not command_flag:
        command = input("コマンドを入力してください (exitで終了): ")
        if command == "exit":
            break

def main() -> None:    
    """
    プログラムのエントリーポイント。
    """
    global command, command_flag
    try:
        serial_params = {
            "port": PORT1,
            "baudrate": BAUD_RATE,
            "party": PARTY,
            "stopbits": STOPBITS,
            "timeout": TIMEOUT,
        }

        test = Instance(serial_params)  # Instanceのインスタンスを作成
        test.main()  # メイン処理を実行

    except KeyboardInterrupt:
        print("プログラムが中断されました.")
    finally:
        pass

if __name__ == "__main__":
    main()  # プログラムの実行
