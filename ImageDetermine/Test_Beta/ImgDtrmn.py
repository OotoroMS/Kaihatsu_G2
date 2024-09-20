# 画像処理のメインプログラム

# ライブラリのインポート
import os
import time
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import numpy as np
import threading

# 自作ライブラリ
import AE_Beta as id_AE

# 定数の定義
JUDGE = {
    "OK": True,
    "NG": False
}

class ImgDtrmn:
    # コンストラクタ
    def __init__(self):
        # 画像処理クラスのインスタンス化
        self.id_AE = id_AE.InferenceModel("ImageDetermine/Test_Beta/model/AE_model.keras")
        self.judge = JUDGE["OK"]

    # これを呼んで実行
    def main(self):
        # 最初に撮影
        self.img_rot_cam()

        # 判別、回転の繰り返し
        while True:
            # スレッド化
            # スレッド1: 画像処理
            thread1 = threading.Thread(target=self.img_dtrmn, args=("./ImageDetermine/Test_Beta/DamagedImages/sample_image.jpg",))
            thread1.start()

            # スレッド2: 画像回転、撮影
            #とりあえず一定間隔でプリント表示
            thread2 = threading.Thread(target=self.thread_test)
            thread2.start()

            # スレッドの終了待ち
            thread1.join()
            thread2.join()

            # 画像の判定
            thread1_result = thread1.result
            if self.threshold_judge(thread1_result, 0.1):
                print("Threshold is exceeded.")
                self.judge = JUDGE["OK"]
            else:
                print("Threshold is not exceeded.")
                self.judge = JUDGE["NG"]
                break
    
    # 画像処理メソッド
    def img_dtrmn(self, image_path):
        # 画像処理の実行
        result = self.id_AE.infer(image_path)
        return result
    
    # 回転、撮影メソッド
    def img_rot_cam(self):
        # 画像の回転、撮影
        return None
    
    # 閾値で判定
    def threshold_judge(self, result, threshold):
        # 判定
        if result["accuracy"] < threshold:
            return True
        else:
            return False

    # ThreadTestMethod
    def thread_test(self):
        #とりあえず一定間隔でプリント表示
        cnt = 0
        for i in range(13):
            strng = "Processing"
            cnt += 1
            cnt %= 4
            for j in range(cnt):
                strng += "."
            print(strng)
            time.sleep(0.2)
        return None
    
if __name__ == "__main__":
    # 画像処理クラスのインスタンス化
    img_dtrmn = ImgDtrmn()

    # 画像処理の実行
    img_dtrmn.main()