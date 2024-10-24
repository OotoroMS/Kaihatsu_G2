from serial_connection import SerialConnection
from process_queue import QueueCreate
import threading
import serial

# シリアルポートの設定
PORT1 = "COM5"  # シリアルポート
BAUD_RATE = 9600  # ボーレート
TIMEOUT = 0.05  # タイムアウト
PARTY = serial.PARITY_EVEN
STOPBITS = serial.STOPBITS_ONE

# グローバル変数
command = None  # 入力されたコマンド
command_flag = False  # コマンドスレッドの終了フラグ

class Instance:
    def __init__(self, params):
        # 各要素のインスタンス化
        queue_creator = QueueCreate()
        self.queues = queue_creator.get_communication_queues()  # キューの取得
        self.serial_conn = SerialConnection(params, self.queues)

    def main(self):
        # スレッドを開始
        self.thread_start()
        self.run_main_loop()

    def thread_start(self):
        if self.serial_conn.serial_comm.is_open:
            # スレッドの作成と開始
            self.send_th = threading.Thread(target=self.serial_conn.process_received_data, daemon=True)
            self.send_th.start()

            self.rcv_th = threading.Thread(target=self.serial_conn.process_send_data, daemon=True)
            self.rcv_th.start()

        # コマンド入力スレッドの開始
        self.cma_th = threading.Thread(target=input_thread, daemon=True)
        self.cma_th.start()

    def run_main_loop(self):
        global command  # コマンドをグローバル変数として使用
        snd_queue = self.queues['send_queue']
        rcv_queue = self.queues['receive_queue']
        
        while True:  # メインループ
            if command == "exit":  # コマンドがexitの場合
                break  # ループを抜ける
            
            if command:  # コマンドがある場合
                snd_queue.put(command)  # コマンドをキューに追加
                command = None  # コマンドをクリア

            if not rcv_queue.empty():  # 受信キューにデータがある場合
                data = rcv_queue.get()
                if data != b'':  # 空のデータでない場合
                    print(f"これが外部に渡すやつ: {data}")

    def thread_stop(self):
        global command_flag  # グローバル変数の使用を宣言
        self.serial_conn.end()    
        command_flag = True  # スレッド終了フラグを設定

        # スレッドを終了させる
        self.send_th.join()
        self.rcv_th.join()
        self.cma_th.join()


def input_thread():
    """コマンド入力スレッド."""
    global command  # グローバル変数を使用
    while not command_flag:
        command = input("コマンドを入力してください (exitで終了): ")
        if command == "exit":
            break

def main():
    """メイン処理."""
    global command, command_flag
    try:
        serial_params = {
            "port": PORT1,
            "baudrate": BAUD_RATE,
            "party": PARTY,
            "stopbits": STOPBITS,
            "timeout": TIMEOUT,         
        }
        # インスタンスを作成して main 関数を呼び出す
        test = Instance(serial_params)
        test.main()

    except KeyboardInterrupt:
        print("プログラムが中断されました.")
    finally:
        pass

if __name__ == "__main__":
    main()  # main関数を実行
