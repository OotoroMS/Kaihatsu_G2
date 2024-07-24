import serial       # シリアル通信モジュールのインポート
import threading    # スレッドモジュールのインポート
import struct       # structモジュールのインポート

# シリアルポートの設定
PORT = "COM4"  # シリアルポート
BAUD_RATE = 9600  # ボーレート 9600
TIMEOUT = 1  # タイムアウト時間

# シリアル通信を管理するクラス
class SerialConnection:
    # 初期化
    def __init__(self, port, baudrate, timeout):
        self.port = port                # シリアルポートの通信ポートを設定
        self.baudrate = baudrate        # ボーレートを設定
        self.timeout = timeout          # タイムアウト時間を設定
        self.send_word = ""             # 送信データの初期値を空に設定
        self.receive_word = ""          # 受信データの初期値を空に設定
        self.serial = None              # シリアルポートオブジェクトの初期値を設定
        self.is_open = False            # シリアルポートが開かれているかのフラグを設定
        self.lock = threading.Lock()    # スレッドの同時アクセスを防ぐためのロックを作成
        self.shutdown_flag = False      # スレッド終了のフラグを初期化

    # シリアルポート接続
    def connect(self):
        try:
            self.serial = serial.Serial(self.port, self.baudrate, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, timeout=self.timeout)  # シリアルポートを開く
            self.is_open = True     # シリアルポートが開かれているフラグを設定
            print(f"シリアルポートに接続しました: {self.serial.name}")  # 接続成功のメッセージを表示
        except serial.SerialException as e:  # シリアルポートの接続エラーをキャッチ
            print(f"シリアルポートの接続エラー: {e}")  # エラーメッセージを表示

    # 送信データ設定
    def set_send_word(self, word):
        with self.lock:  # ロックを使用してスレッドセーフを確保
            if isinstance(word, str):
                self.send_word = word.encode('utf-8')  # 送信するデータを設定
                print(f"str->byte:{word}->{self.send_word}")
            elif isinstance(word, int):                                
                self.send_word = struct.pack('>B', word)    # 送信データを設定
                print(f"int->byte:{word}->{self.send_word}")
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
                    data = self.serial.readline()  # データを受信する
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
