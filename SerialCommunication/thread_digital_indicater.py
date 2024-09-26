from serial_thread import SerialConnection
import threading
import serial_digital_indicator
import time

# シリアル通信用定数
PORT1 = "COM6"      # ポート番号
PORT2 = "COM7"
BAUD_RATE1 = 2400   # ボーレート 2400 インジケータ用
BAUD_RATE2 = 9600   # ボーレート 9600 PLC用 
TIMEOUT = 1       # タイムアウト時間

#   グローバル変数
#   アスキーコード
ASCII_PLAS  = 43
ASCII_MINUS = 45
ASCII_CR    = 13
ASCII_ZERO  = 48
ASCII_DECI  = 46
#   判定基準
PLAS_JUDGMENT  = 0.1
MINUS_JUDGMENT = -0.1
#   判定結果
OK         = True
NG         = False
DATA_SND_MSG = b's'

# コマンド入力
command = None  # 入力されたコマンドを格納する変数
command_flag = False  # コマンドスレッドの終了を示すフラグ

# コマンド入力
def input_thread():
    global command  # グローバル変数を使用
    while not command_flag:  # 終了フラグが設定されるまでループ
        command = input("コマンドを入力してください (exitで終了): ")  # コマンドを入力
        if command == "exit":  # コマンドがexitの場合
            break  # ループを抜ける

if __name__ == '__main__':
    try:
        # シリアルポートに接続してスレッドを開始
        serial_conn1 = SerialConnection(PORT1, BAUD_RATE1, TIMEOUT)  #シリアル接続オブジェクトを作成
        serial_conn1.connect()  # シリアルポートに接続
        # シリアルポートに接続してスレッドを開始
        serial_conn2 = SerialConnection(PORT2, BAUD_RATE2, TIMEOUT)  #シリアル接続オブジェクトを作成
        serial_conn2.connect()  # シリアルポートに接続

        if serial_conn1.is_open and serial_conn2.is_open:
            # 受信用スレッド開始
            receive_thread1 = threading.Thread(target=serial_conn1.receive_data)
            receive_thread1.start()

            # 送信用スレッド開始
            send_thread1 = threading.Thread(target=serial_conn1.send_data)
            send_thread1.start()
            
            # 受信用スレッド開始
            receive_thread2 = threading.Thread(target=serial_conn2.receive_data)
            receive_thread2.start()

            # 送信用スレッド開始
            send_thread2 = threading.Thread(target=serial_conn2.send_data)
            send_thread2.start()

            # 通信可能まで3秒待機
            print("待機中")
            time.sleep(3)
            print("待機終了")

            input_thread = threading.Thread(target=input_thread)  # コマンド入力スレッドを作成
            input_thread.start()  # コマンド入力スレッドを開始

        while True:
            if command == "exit":  # コマンドがexitの場合
                break  # ループを抜ける
            elif command:  # コマンドがある場合
                serial_conn1.set_send_word(DATA_SND_MSG)
                serial_conn2.set_send_word(command)
                command = None  # コマンドをクリア
            
            # データを受信
            data1 = serial_conn1.get_receive_word()
            data2 = serial_conn2.get_receive_word()
            # 受信データ有
            if data1:
                meas_val = serial_digital_indicator.chenge_byte_float(data1)
                print("受信データ:", data1, "測定値:", meas_val)
            if data2:
                print(f"data2:{data2.decode()}")
            


    except KeyboardInterrupt:
        print("プログラムが中断されました.")  # 中断メッセージを表示
    finally:
        # シリアル通信終了フラグON
        serial_conn1.shutdown_flag = True

        # シリアル通信終了フラグON
        serial_conn2.shutdown_flag = True

        command_flag = True  # コマンドスレッドの終了フラグを設定

        # 受信スレッド終了待ち
        receive_thread1.join()

        # 送信スレッド終了待ち
        send_thread1.join()

        # 受信スレッド終了待ち
        receive_thread2.join()

        # 送信スレッド終了待ち
        send_thread2.join()

        input_thread.join()  # コマンドスレッドの終了を待機    

        # シリアルポートが開いている場合
        if serial_conn1.is_open:
            serial_conn1.close()     # シリアルポートを閉じる
        if serial_conn2.is_open:
            serial_conn2.close()

        print("プログラム終了")