# PLCとの通信用

# ライブラリのインポート
import serial
import time

# グローバル変数
STATE = {
    "START": "START",
    "STOP": "STOP",
}

class PLC_Lib:
    STATE = STATE  # 外部からアクセスできるようにクラス変数として定義

    def __init__(self, port='COM1', baudrate=9600):
        # PLCの設定
        try:
            self.ser = serial.Serial(port, baudrate, timeout=1)
            time.sleep(2)  # ポートの初期化待ち
        except serial.SerialException:
            print("!ERR! PLCとの接続に失敗しました。")
            exit()

    def get_data(self):
        # PLCからデータを取得
        if self.ser.in_waiting > 0:
            data = self.ser.readline().decode('utf-8').strip()
            return data
        else:
            return None

    def send_data(self, data):
        # PLCにデータを送信
        send_str = (data + '\n').encode('utf-8')
        self.ser.write(send_str)

    def release(self):
        # PLCのリソースを解放
        self.ser.close()
