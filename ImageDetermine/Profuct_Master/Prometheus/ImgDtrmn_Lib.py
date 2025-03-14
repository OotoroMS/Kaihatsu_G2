# 画像処理関連のライブラリ
import os
import datetime
import cv2
import glob
import numpy as np
import tensorflow as tf
from sklearn.preprocessing import robust_scale

class ImgDtrmn_Lib:
    def __init__(self, model_path, crop_ranges, workname="test_work"):
        ### 初期化処理 ###
        self.workname = workname
        self.model_path = model_path
        self.model = None
        self.input_shape = None
        self.output_shape = None
        self.model_name = None
        self.crop_ranges = crop_ranges
        
        # DB格納先パス
        self.infered_img_path = "results/infered_images" # 推論画像の保存先 result_dir/infered_images/[self.workname]/YY_MM_DD/HH_MM_SS.png

    def load_model(self):
        # モデルのロード
        self.model = tf.keras.models.load_model(self.model_path)
        self.input_shape = self.model.input_shape
        self.output_shape = self.model.output_shape
        self.model_name = self.model.name

    # おそらく完成
    def robust_scale_image(self, image):
        """
        画像をロバストスケーリングするユーティリティ関数。
        1. 画像をfloat型に変換
        2. Flattenしてrobust_scaleを適用
        3. 元の形状にreshape
        4. ピクセル値の範囲が負になる場合は、適当なスケーリング/クリッピングを行う
        """
        float_img = image.astype(np.float32)
        flat_img = float_img.flatten()
        scaled_flat = robust_scale(flat_img)  # 中央値0, IQRで正規化される
        # robust_scaleの結果が負になることがあるため、0-255に収めるために再スケーリング
        # min/maxを取り、[0,255] に押し込む例
        min_val = scaled_flat.min()
        max_val = scaled_flat.max()
        
        # 分母が0の場合を考慮
        if max_val == min_val:
            print("!WARN! 画像が単一値で構成されています。スケーリングをスキップします。")
            scaled_flat = flat_img  # スケーリングせず元の値を使用
        else:
            scaled_flat = (scaled_flat - min_val) / (max_val - min_val) * 255.0
        
        scaled_img = scaled_flat.reshape(float_img.shape).astype(np.uint8)
        return scaled_img


    def pre_processing(self, tmp_img):
        """
        画像の前処理:
            引数:
                tmp_img: 入力画像
            戻り値:
                done_img: 前処理済み画像
            
            処理:
                1. 画像をクロップ
                2. ロバストスケーリング
                3. ガウスフィルタ
                4. メジアンフィルタ
        """
        # 1. クロップ
        print("クロップ範囲: ", self.crop_ranges)
        print("画像サイズ: ", tmp_img.shape)
        cropped = tmp_img[self.crop_ranges["y_start"]:self.crop_ranges["y_end"], self.crop_ranges["x_start"]:self.crop_ranges["x_end"]]
        if cropped.size == 0:
            raise ValueError("クロップ後の画像が空です。クロップ範囲を確認してください。")
        
        # 1-1. 縮小(縦横それぞれ1/4にする)
        cropped = cv2.resize(cropped, (cropped.shape[1] // 4, cropped.shape[0] // 4), interpolation=cv2.INTER_AREA)        

        # 2. ロバストスケーリング
        array_cropped = np.array(cropped)
        scaled = self.robust_scale_image(array_cropped)
        
        # 3. ガウスフィルタ
        # ksize=(5,5), sigmaX=0などは例示。任意に変更可能
        gaussian = cv2.GaussianBlur(scaled, (5, 5), 0)
        
        # 4. メジアンフィルタ
        # ksize=5を例示
        median = cv2.medianBlur(gaussian, 5)

        return median

    def inference(self, inpt_img):
        """
        画像の推論:
            引数:
                inpt_img: 入力画像
            戻り値:
                mse: MSE
                infered_img: 推論画像
        """
        # モデルの期待する形状にリシェイプ
        inpt_img = inpt_img.reshape((1, -1))  # 入力を1次元に整形
        # 推論
        infered_img = self.model.predict(inpt_img)
        infered_img = infered_img.reshape(-1)  # 推論結果をフラット化

        # 入力画像もフラット化
        inpt_img_flat = inpt_img.flatten()

        # 両者の形状を確認
        #print(f"推論後の形状: {infered_img.shape}, 入力画像の形状: {inpt_img_flat.shape}")

        # MSEの計算
        mse = np.mean((infered_img - inpt_img_flat[:infered_img.size]) ** 2)

        # 推論画像とMSEを返す
        return mse, infered_img

    # 要検討
    def mark_defects(self, input_img, infered_img):
        """
        不良箇所をマークする:
            引数:
                input_img: 入力画像（前処理済み）
                infered_img: 推論された画像
            戻り値:
                marked_img: 不良箇所をマークした画像
        """
        # input_imgの形状をarrayに変換
        input_img = np.array(input_img)
        # 推論画像の形状を元の画像に変換
        infered_img = infered_img.reshape(input_img.shape)

        # 入力画像と推論画像の両方を1チャンネルに変換
        input_img = input_img.reshape((1,) + input_img.shape)

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
