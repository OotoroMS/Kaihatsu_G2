import cv2
import numpy as np
from tensorflow.keras.models import load_model

def is_scratch_image(image_path, model_name):
    # モデルの読み込み
    model = load_model(model_name)
    
    # 画像を読み込んでグレースケールに変換
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    
    # 画像を正規化し、モデルに適した形状にリサイズ
    image = image.astype('float32') / 255.0
    image = np.expand_dims(image, axis=-1)  # チャンネル次元を追加
    image = np.expand_dims(image, axis=0)   # バッチ次元を追加

    # モデルで予測
    reconstructed = model.predict(image)

    # 再構成誤差を計算
    mse = np.mean(np.power(image - reconstructed, 2), axis=(1, 2, 3))

    # 閾値を設定して、傷の有無を判別
    threshold = 0.01  # 適切なしきい値を設定
    return mse > threshold
