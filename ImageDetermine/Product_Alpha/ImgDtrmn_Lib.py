# 画像処理関連のライブラリ

import cv2
import numpy as np
import tensorflow as tf

class ImgDtrmn_Lib:
    def __init__(self, model_path='model.h5', crop_ranges=None):
        ### 初期化処理 ###
        self.model_path = model_path
        self.model = None
        self.input_shape = None
        self.output_shape = None
        self.model_name = None
        self.crop_ranges = crop_ranges  # 追加

    def load_model(self):
        # モデルのロード
        self.model = tf.keras.models.load_model(self.model_path)
        self.input_shape = self.model.input_shape
        self.output_shape = self.model.output_shape
        self.model_name = self.model.name

    def pre_processing(self, tmp_img):
        """
        画像の前処理:
            引数:
                tmp_img: 入力画像
            戻り値:
                done_img: 前処理済み画像
            
            処理:
                1. 画像をクロップ
                2. 画像をノーマライズ
                3. バッチ次元を追加
        """
        if self.crop_ranges:
            x_start = self.crop_ranges.get('x_start', 0)
            x_end = self.crop_ranges.get('x_end', tmp_img.shape[1])
            y_start = self.crop_ranges.get('y_start', 0)
            y_end = self.crop_ranges.get('y_end', tmp_img.shape[0])
            # 画像をクロップ
            cropped_img = tmp_img[y_start:y_end, x_start:x_end]
        else:
            cropped_img = tmp_img

        # ノーマライズ
        norm_img = cropped_img / 255.0

        # リサイズ（モデルの入力サイズに合わせる）
        input_height = self.input_shape[1]
        input_width = self.input_shape[2]
        resized_img = cv2.resize(norm_img, (input_width, input_height))

        # バッチ次元を追加
        done_img = np.expand_dims(resized_img, axis=0)

        return done_img

    def inference(self, inpt_img):
        """
        画像の推論:
            引数:
                inpt_img: 入力画像
            戻り値:
                mse: MSE
                infered_img: 推論画像
            
            処理:
                1. 画像を推論
                2. MSEで精度を検出
        """
        # 画像を推論
        infered_img = self.model.predict(inpt_img)

        # MSEで精度を検出
        mse = np.mean((infered_img - inpt_img) ** 2)

        return mse, infered_img

    def mark_defects(self, input_img, infered_img):
        """
        不良箇所をマークする:
            引数:
                input_img: 入力画像（前処理済み）
                infered_img: 推論された画像
            戻り値:
                marked_img: 不良箇所をマークした画像
        """
        # 入力画像と推論画像の差分を計算
        diff = np.abs(input_img - infered_img)

        # 差分をしきい値処理
        threshold = 0.1  # 差分の閾値は調整が必要
        diff[diff < threshold] = 0
        diff[diff >= threshold] = 1

        # 差分を3チャンネルに拡張
        diff = np.squeeze(diff, axis=0)  # バッチ次元を削除
        diff_color = np.stack((diff, np.zeros_like(diff), np.zeros_like(diff)), axis=-1)  # 赤色で表示

        # 元の入力画像をカラーに変換
        input_img_color = np.squeeze(input_img, axis=0)
        input_img_color = cv2.cvtColor(input_img_color.astype('float32'), cv2.COLOR_GRAY2BGR)

        # 不良箇所をマーク
        marked_img = cv2.addWeighted(input_img_color, 1.0, diff_color.astype('float32'), 0.5, 0)

        # 画像を0-255にスケーリング
        marked_img = (marked_img * 255).astype('uint8')

        return marked_img
