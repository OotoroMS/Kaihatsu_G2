import serial
import time

# シリアルポートの設定
ser = serial.Serial('COM10', 9600)

# データを送信する関数
def send_data(data):
    ser.write(data.encode('utf-8'))
    print(f'Sent: {data}')

# メインの処理
try:
    while True:
        message = input("送信するメッセージを入力してください (終了する場合は q を入力): ")
        if message.lower() == 'q':
            break
        send_data(message)
        time.sleep(1)  # 送信ごとに1秒間のインターバルを設ける例
except KeyboardInterrupt:
    pass
finally:
    ser.close()
    print("シリアルポートを閉じました。")
