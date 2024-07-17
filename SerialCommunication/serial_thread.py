import serial  # シリアル通信モジュールのインポート
import threading  # スレッドモジュールのインポート
import time  # 時間モジュールのインポート

# シリアルポートの設定
PORT1 = "COM4"  # 最初のシリアルポート
PORT2 = "COM5"  # 二番目のシリアルポート
BAUD_RATE = 9600  # ボーレート 9600
TIMEOUT = 1  # タイムアウト時間

command = None  # 入力されたコマンドを格納する変数
command_flag = False  # コマンドスレッドの終了を示すフラグ

# シリアル通信を管理するクラス
class SerialConnection:
    # 初期化
    def __init__(self, port, baudrate, timeout):
        self.port = port  # シリアルポートの通信ポートを設定
        self.baudrate = baudrate  # ボーレートを設定
        self.timeout = timeout  # タイムアウト時間を設定
        self.send_word = ""  # 送信データの初期値を空に設定
        self.receive_word = "" # 受信データの初期値を空に設定
        self.serial = None  # シリアルポートオブジェクトの初期値を設定
        self.is_open = False  # シリアルポートが開かれているかのフラグを設定
        self.lock = threading.Lock()  # スレッドの同時アクセスを防ぐためのロックを作成
        self.shutdown_flag = False  # スレッド終了のフラグを初期化

    # シリアルポート接続
    def connect(self):
        try:
            self.serial = serial.Serial(self.port, self.baudrate, timeout=self.timeout)  # シリアルポートを開く
            self.is_open = True  # シリアルポートが開かれているフラグを設定
            print(f"シリアルポートに接続しました: {self.serial.name}")  # 接続成功のメッセージを表示
        except serial.SerialException as e:  # シリアルポートの接続エラーをキャッチ
            print(f"シリアルポートの接続エラー: {e}")  # エラーメッセージを表示

    # 送信データ設定
    def set_send_word(self, word):
        with self.lock:  # ロックを使用してスレッドセーフを確保
            if isinstance(word, str):
                print(f"文字列:{word}")
                self.send_word = word.encode('utf-8')  # 送信するデータを設定
                print(f"バイト列:{self.send_word}")
            elif isinstance(word, bytes):
                self.send_word = word

    # データ送信
    def send_data(self):
        try:
            while not self.shutdown_flag:  # 終了フラグが設定されるまでループ
                if self.is_open and self.send_word:  # シリアルポートが開いていて送信データがある場合
                    with self.lock:  # ロックを使用してスレッドセーフを確保
                        self.serial.write(self.send_word)  # データをシリアルポートに送信
                        print(f"データを送信しました: {self.send_word}")  # 送信成功のメッセージを表示
                        self.send_word = ""  # 送信データをクリア
                time.sleep(0.1)  # 少し待機
        except serial.SerialException as e:  # 送信エラーをキャッチ
            print(f"シリアルポートの送信エラー ({self.serial.name}): {e}")  # エラーメッセージを表示

    # 受信データ取得
    def get_receive_word(self):
        data = ""               # dataを初期化       
        if self.receive_word:  # 受信データがある場合 
            data = self.receive_word    # 受信データを代入
            self.receive_word = ""      # 受信データクリア
            print(f"receive_word : {data}")  # データを表示            
            return data  # データを返す
        
    # データ受信
    def receive_data(self):
        try:
            while not self.shutdown_flag:  # 終了フラグが設定されるまでループ
                if self.is_open:  # シリアルポートが開かれている場合
                    data = self.serial.read(255).strip()  # データを受信する
                    if data:  # データがある場合                        
                        print(f"受信したデータ ({self.serial.name}): {data}")  # 受信データを表示
                        self.receive_word = data  # 受信データを保存
        except serial.SerialException as e:  # 受信エラーをキャッチ
            print(f"シリアルポートの受信エラー ({self.serial.name}): {e}")  # エラーメッセージを表示

    # シリアルポート閉じる
    def close(self):
        if self.serial and self.serial.is_open:  # シリアルポートが開かれている場合
            print(f"シリアルポートをクローズしました: {self.serial.name}")  # クローズメッセージを表示
            self.serial.close()  # シリアルポートを
            self.is_open = False  # シリアルポートの開閉状態を更新
        else:
            print(f"シリアルポートが正しく開かれていません。({self.serial.name})")  # エラーメッセージを表示

        self.serial = None  # シリアルポートオブジェクトをNoneに設定

# コマンド入力
def input_thread():
    global command  # グローバル変数を使用
    while not command_flag:  # 終了フラグが設定されるまでループ
        command = input("コマンドを入力してください (exitで終了): ")  # コマンドを入力
        if command == "exit":  # コマンドがexitの場合
            break  # ループを抜ける

if __name__ == "__main__":
    try:        
        # シリアルポートに接続してスレッドを開始
        serial_conn1 = SerialConnection(PORT1, BAUD_RATE, TIMEOUT)  # 最初のシリアル接続オブジェクトを作成
        serial_conn2 = SerialConnection(PORT2, BAUD_RATE, TIMEOUT)  # 二番目のシリアル接続オブジェクトを作成

        serial_conn1.connect()  # 最初のシリアルポートに接続
        serial_conn2.connect()  # 二番目のシリアルポートに接続

        input_thread = threading.Thread(target=input_thread)  # コマンド入力スレッドを作成
        input_thread.start()  # コマンド入力スレッドを開始

        if serial_conn1.is_open and serial_conn2.is_open:  # 両方のシリアルポートが開かれている場合
            receive_thread1 = threading.Thread(target=serial_conn1.receive_data)  # 最初の受信スレッドを作成
            receive_thread1.start()  # 最初の受信スレッドを開始

            receive_thread2 = threading.Thread(target=serial_conn2.receive_data)  # 二番目の受信スレッドを作成
            receive_thread2.start()  # 二番目の受信スレッドを開始

            send_thread1 = threading.Thread(target=serial_conn1.send_data)  # 最初の送信スレッドを作成
            send_thread2 = threading.Thread(target=serial_conn2.send_data)  # 二番目の送信スレッドを作成
        
            send_thread1.start()  # 最初の送信スレッドを開始
            send_thread2.start()  # 二番目の送信スレッドを開始

        while True:  # メインループ
            if command == "exit":  # コマンドがexitの場合
                break  # ループを抜ける
            elif command:  # コマンドがある場合
                serial_conn1.set_send_word(command)  # 最初のシリアルポートにコマンドを設定
                serial_conn2.set_send_word(command)  # 二番目のシリアルポートにコマンドを設定
                command = None  # コマンドをクリア

            data1 = serial_conn1.get_receive_word()  # 最初の受信データを取得
            if data1:  # データがある場合
                print(f"data1 : {data1}")  # データを表示
                data1 = ""
            data2 = serial_conn2.get_receive_word()  # 二番目の受信データを取得
            if data2:  # データがある場合
                print(f"data2 : {data2}")  # データを表示
                data2 = ""

    except KeyboardInterrupt:  # キーボード割り込み（Ctrl+C）をキャッチ
        print("プログラムが中断されました.")  # 中断メッセージを表示
    finally:
        serial_conn1.shutdown_flag = True  # 最初のシリアル接続の終了フラグを設定
        serial_conn2.shutdown_flag = True  # 二番目のシリアル接続の終了フラグを設定

        command_flag = True  # コマンドスレッドの終了フラグを設定

        while receive_thread1.join() and receive_thread2.join():  # 受信スレッドの終了を待機
            pass
        print("受信スレッド終了")  # 受信スレッドの終了を表示

        while send_thread1.join() and send_thread2.join():  # 送信スレッドの終了を待機
            pass
        print("送信スレッド終了")  # 送信スレッドの終了を表示

        print("何かしら入力してください")  # 入力待機メッセージを表示
        input_thread.join()  # コマンドスレッドの終了を待機
        print("コマンドスレッド終了")  # コマンドスレッドの終了を表示

        if serial_conn1.is_open:  # 最初のシリアルポートが開かれている場合
            serial_conn1.close()  # 最初のシリアルポートをクローズ
        if serial_conn2.is_open:  # 二番目のシリアルポートが開かれている場合
            serial_conn2.close()  # 二番目のシリアルポートをクローズ

        print("プログラムを終了します.")  # プログラム終了メッセージを表示
