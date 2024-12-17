import cv2
import os
import json
import numpy as np  # NumPyをインポート
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# データ拡張の設定
datagen = ImageDataGenerator(
    rotation_range=10,  # 回転の範囲
    width_shift_range=0.05,  # 水平方向のシフト範囲
    height_shift_range=0.05,  # 垂直方向のシフト範囲
    zoom_range=0.1,  # 拡大縮小の範囲
    horizontal_flip=False,  # 水平反転
    vertical_flip=False,  # 垂直反転
    fill_mode='nearest'
)

# 保存ディレクトリとカウンター保存ファイル
save_dir = 'captured_images'
counter_file = 'image_counter.json'
os.makedirs(save_dir, exist_ok=True)

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

while True:
    # カメラからフレームを取得
    ret, frame = cap.read()
    if not ret:
        print("Failed to capture image")
        break

    # フレームを1/2縮尺で表示
    display_frame = cv2.resize(frame, (frame.shape[1] // 2, frame.shape[0] // 2))
    cv2.putText(display_frame, f'Images Captured: {counter["count"]}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.imshow('Camera', display_frame)

    # キー入力を待つ
    key = cv2.waitKey(1)
    if key == ord('q'):
        break
    elif key == ord(' '):
        # スペースキーが押された場合
        image_path = os.path.join(save_dir, f'image_{counter["count"]:04d}.jpg')
        cv2.imwrite(image_path, frame)
        
        # データ拡張を適用
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        image = np.expand_dims(image, -1)  # チャンネル次元の追加
        image = np.expand_dims(image, 0)  # バッチ次元の追加
        augmented_iter = datagen.flow(image, batch_size=1, save_to_dir=save_dir, save_prefix=f'aug_{counter["count"]:04d}', save_format='jpg')
        
        # 5枚の拡張画像を生成
        for i in range(5):
            next(augmented_iter)

        # カウンターを更新
        counter['count'] += 1
        with open(counter_file, 'w') as f:
            json.dump(counter, f)

# リソースを解放
cap.release()
cv2.destroyAllWindows()
