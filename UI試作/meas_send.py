from serial_thread_2 import SerialConnection
import threading

# シリアル通信用定数
Port = "COM10"       # 
Baud_Rate = 9600    # ボーレート 9600
TimeOut = 1         # タイムアウト時間

# 検証用文字列
data_rcv_msg = b"01A+00001.23\r"

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

        while True:
            # データを受信
            data = serial_conn.get_receive_word()
            # 受信データ有
            if data:
                # 文字列をbyteに変換
                print("受信データ:", data)
                if data == b's':
                    # 検証用文字列を送信
                    serial_conn.set_send_word(data_rcv_msg)
                # データを初期化
                data = ""


    except KeyboardInterrupt:
        print("プログラムが中断されました.")  # 中断メッセージを表示
    finally:
        # シリアル通信終了フラグON
        serial_conn.shutdown_flag = True

        # 受信スレッド終了待ち
        receive_thread.join()

        # 送信スレッド終了待ち
        send_thread.join()

        # シリアルポートが開いている場合
        if serial_conn.is_open:
            serial_conn.close()     # シリアルポートを閉じる

        print("プログラム終了")