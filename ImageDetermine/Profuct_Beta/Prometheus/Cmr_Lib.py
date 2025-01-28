# カメラのドライバー

import cv2
import numpy as np

class Cmr_Lib:
    def __init__(self, camera_num=0):
        # カメラの設定
        self.cap = cv2.VideoCapture(camera_num)
        if not self.cap.isOpened():
            print("!ERR! カメラの初期化に失敗しました。")
            exit()

    def get_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            print("!ERR! フレームの取得に失敗しました。")
            return None
        
        print(frame.shape)  # デバッグ用：画像の形状を表示
        
        if frame.shape[2] == 3:
            # BGRの場合
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        elif frame.shape[2] == 2:
            # 2チャンネルの場合
            frame = frame[:,:,0]  # 最初のチャンネルのみを使用
        elif frame.shape[2] == 1:
            # すでにグレースケールの場合
            pass
        else:
            print(f"!ERR! 未対応のチャンネル数: {frame.shape[2]}")
            return None

        return frame

    def detect_exist(self, trgt_img, init_img, threshold=500000):
        """
        画像を取得し、存在判定を行う
            引数:
                trgt_img: 現在の画像
                init_img: 初期状態の背景画像
                threshold: 差分の閾値
            戻り値:
                is_exist: 存在判定（True: 存在する、False: 存在しない）

            処理:
                1. 2つの画像の差分を計算
                2. 差分画像のピクセル値の総和を計算
                3. 閾値と比較して存在を判定
        """
        # 取得した画像のshapeを確認
        if trgt_img.shape != init_img.shape:
            print("!ERR! 画像の形状が異なります。")
            return None

        # 差分を計算
        diff_img = cv2.absdiff(trgt_img, init_img)

        # 差分のピクセル値の総和を計算
        diff_sum = np.sum(diff_img)

        # 存在を判定
        if diff_sum > threshold:
            return True  # オブジェクトが存在する
        else:
            return False  # オブジェクトは存在しない

    def release(self):
        self.cap.release()
        cv2.destroyAllWindows()
