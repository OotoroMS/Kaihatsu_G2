from serial_thread_2 import SerialConnection
import threading
import meas_test
import time

# シリアル通信用定数
Port = "COM6"       # 
Baud_Rate = 2400    # ボーレート 9600
TimeOut = 0.1         # タイムアウト時間

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
DATA_SND_MSG = 's'

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
        serial_conn = SerialConnection(Port, Baud_Rate, TimeOut)  #シリアル接続オブジェクトを作成
        serial_conn.connect()  # シリアルポートに接続

        if serial_conn.is_open:
            # 受信用スレッド開始
            receive_thread = threading.Thread(target=serial_conn.receive_data)
            receive_thread.start()

            # 送信用スレッド開始
            send_thread = threading.Thread(target=serial_conn.send_data)
            send_thread.start()

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
                serial_conn.set_send_word(DATA_SND_MSG)
                command = None  # コマンドをクリア
            
            # データを受信
            data = serial_conn.get_receive_word()
            # 受信データ有
            if data:
                meas_val = meas_test.chenge_byte_float(data)
                print("受信データ:", data, "測定値:", meas_val)


    except KeyboardInterrupt:
        print("プログラムが中断されました.")  # 中断メッセージを表示
    finally:
        # シリアル通信終了フラグON
        serial_conn.shutdown_flag = True

        command_flag = True  # コマンドスレッドの終了フラグを設定

        # 受信スレッド終了待ち
        receive_thread.join()

        # 送信スレッド終了待ち
        send_thread.join()

        input_thread.join()  # コマンドスレッドの終了を待機    

        # シリアルポートが開いている場合
        if serial_conn.is_open:
            serial_conn.close()     # シリアルポートを閉じる

        print("プログラム終了")