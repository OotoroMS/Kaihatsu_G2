import cv2
import os
import json
import numpy as np
import time
from datetime import datetime
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from serial_connection import SerialConnection  # 前回作成したクラスをインポート

# シリアルポートの設定
PORT1 = "COM3"
BAUD_RATE = 9600
TIMEOUT = 1

# データ拡張の設定
datagen = ImageDataGenerator(
    rotation_range=10,
    width_shift_range=0.05,
    height_shift_range=0.05,
    zoom_range=0.1,
    horizontal_flip=False,
    vertical_flip=False,
    fill_mode='nearest'
)

# 保存ディレクトリの設定
original_dir = 'tmp'
augmented_dir = 'tmp'
counter_file = 'image_counter.json'
os.makedirs(original_dir, exist_ok=True)
os.makedirs(augmented_dir, exist_ok=True)

# カウンターの読み込みまたは初期化
if os.path.exists(counter_file):
    with open(counter_file, 'r') as f:
        counter = json.load(f)
else:
    counter = {'count': 0}

# カメラを初期化
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 2592)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1944)

# シリアルポート接続
serial_conn = SerialConnection(PORT1, BAUD_RATE, TIMEOUT)
serial_conn.connect()
serial_conn.start_communication()

try:
    for i in range(26):
        # シリアルポートに「1」を送信
        serial_conn.set_send_word(20)
        serial_conn.set_send_word(10)
        time.sleep(1.0)  # シリアル送信後の待機時間（必要に応じて調整）

        # カメラからフレームを取得
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture image")
            break

        # 画像を現在時刻で保存
        current_time = datetime.now().strftime('%Y%m%d_%H%M%S')
        original_image_path = os.path.join(original_dir, f'image_{current_time}.jpg')
        cv2.imwrite(original_image_path, frame)

        # データ拡張を適用
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        image = np.expand_dims(image, -1)  # チャンネル次元の追加
        image = np.expand_dims(image, 0)  # バッチ次元の追加
        augmented_iter = datagen.flow(image, batch_size=1, save_to_dir=augmented_dir, save_prefix=f'aug_{current_time}', save_format='jpg')
        
        # 5枚の拡張画像を生成
        #for _ in range(5):
        #    next(augmented_iter)

        # カウンターを更新
        counter['count'] += 1
        with open(counter_file, 'w') as f:
            json.dump(counter, f)

        # 簡単なログ出力
        print(f"Captured and saved image {i+1}/26: {original_image_path}")

        time.sleep(1)  # 次のループまでの待機時間（必要に応じて調整）

except KeyboardInterrupt:
    print("Program interrupted.")
finally:
    # リソースを解放
    cap.release()
    cv2.destroyAllWindows()
    serial_conn.stop_communication()
    print("Program terminated.")
