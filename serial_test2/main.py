import time
from process_queue import queue
import serial
from serial_connection import SerialConnection
import threading

# シリアルポートの設定
PORT1 = "COM5"  # 最初のシリアルポート
BAUD_RATE = 9600  # ボーレート 9600
TIMEOUT = 0.05  # タイムアウト時間
PARTY = serial.PARITY_EVEN
STOPBITS = serial.STOPBITS_ONE

command = None  # 入力されたコマンドを格納する変数
command_flag = False  # コマンドスレッドの終了を示すフラグ


# コマンド入力
def input_thread():
    global command  # グローバル変数を使用
    while not command_flag:  # 終了フラグが設定されるまでループ
        command = input("コマンドを入力してください (exitで終了): ")  # コマンドを入力
        if command == "exit":  # コマンドがexitの場合
            break  # ループを抜ける

if __name__ == "__main__":
    try:
        test = queue()        
        snd_queue, rcv_queue, degital_queue, user_queue = test.get_queue()
        serial_params = {
            "port":PORT1,
            "baudrate":BAUD_RATE,
            "party":PARTY,
            "stopbits":STOPBITS,
            "timeout":TIMEOUT,
            "snd_queue": snd_queue,
            "rcv_queue": rcv_queue
        }
        command_thread = threading.Thread(target=input_thread)
        command_thread.start()
        # シリアルポートに接続してスレッドを開始
        serial_conn1 = SerialConnection(**serial_params)  # 最初のシリアル接続オブジェクトを作成                

        if serial_conn1.serial_comm.is_open:  # シリアルポートが開かれている場合
            receive_thread1 = threading.Thread(target=serial_conn1.process_received_data)  # 最初の受信スレッドを作成
            receive_thread1.start()  # 最初の受信スレッドを開始

            send_thread1 = threading.Thread(target=serial_conn1.process_send_data)  # 最初の送信スレッドを作成      
        
            send_thread1.start()  # 最初の送信スレッドを開始

            while True:  # メインループ
                if command == "exit":  # コマンドがexitの場合
                    break  # ループを抜ける
                if command:  # コマンドがある場合
                    snd_queue.put(command)  # ここでコマンドをキューに追加
                    command = None  # コマンドをクリア

                if not rcv_queue.empty():
                    data = rcv_queue.get()
                    if b'' != data:
                        print(f"これが外部に渡すやつ{data}")

    except KeyboardInterrupt:  # キーボード割り込み（Ctrl+C）をキャッチ
        print("プログラムが中断されました.")  # 中断メッセージを表示
    finally:                        
        serial_conn1.end()    
        command_flag = True
        send_thread1.join()
        receive_thread1.join()
        command_thread.join()
        print("プログラムを終了します.")  # プログラム終了メッセージを表示