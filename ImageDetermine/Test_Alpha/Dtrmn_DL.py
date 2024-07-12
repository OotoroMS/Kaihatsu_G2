import os
import cv2
import numpy as np
from ultralytics import YOLO

class DeepLearning:
    # コンストラクタ
    def __init__(self):
        # YOLOv5の初期化
        self.yolo = YOLO("ImageDetermine/Test_Alpha/yolov8n.pt")

    # ディープラーニングで判別
    def determine(self, img):
        # グレースケール画像を3チャンネルに変換
        if len(img.shape) == 2:
            img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
        
        # 画像の解像度を取得
        height, width = img.shape[:2]
        print(f"Image resolution: {width}x{height}")

        # ガウシアンブラーを適用してノイズを除去
        img = cv2.GaussianBlur(img, (5, 5), 0)

        # 画像をリサイズ
        img_resized = cv2.resize(img, (416, 416))

        # YOLOv5で物体検出
        results = self.yolo.predict(img_resized)

        # 結果を描画
        for result in results:
            boxes = result.boxes.xyxy.cpu().numpy().astype(int)
            classes = result.boxes.cls.cpu().numpy().astype(int)
            for box, cls in zip(boxes, classes):
                # バウンディングボックスを描画
                cv2.rectangle(img, (box[0], box[1]), (box[2], box[3]), (0, 255, 0), 2)
                # クラスラベルを取得
                class_name = self.yolo.names[int(cls)]
                # クラスラベルを描画（バウンディングボックスの内側に）
                label_size, base_line = cv2.getTextSize(class_name, cv2.FONT_HERSHEY_SIMPLEX, 0.9, 2)
                top_left_corner = (box[0], box[1])
                bottom_right_corner = (box[0] + label_size[0], box[1] + label_size[1] + base_line)
                cv2.rectangle(img, top_left_corner, bottom_right_corner, (0, 255, 0), cv2.FILLED)
                cv2.putText(img, class_name, (box[0], box[1] + label_size[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 0), 2)

        return img

# 画像の差分を計算して変化があった領域を検出
def detect_changes(prev_img, current_img):
    # グレースケールに変換
    prev_gray = cv2.cvtColor(prev_img, cv2.COLOR_BGR2GRAY)
    current_gray = cv2.cvtColor(current_img, cv2.COLOR_BGR2GRAY)

    # 画像の差分を計算
    diff = cv2.absdiff(prev_gray, current_gray)

    # 差分画像を二値化
    _, thresh = cv2.threshold(diff, 75, 255, cv2.THRESH_BINARY)  # しきい値を調整

    # 輪郭を検出
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # 変化があった領域を赤色で描画
    change_detected = False
    for contour in contours:
        if cv2.contourArea(contour) > 1000:  # ノイズを除去するために最小面積を設定
            change_detected = True
            x, y, w, h = cv2.boundingRect(contour)
            current_img[y:y+h, x:x+w] = np.where(thresh[y:y+h, x:x+w][:, :, None] == 255, (0, 0, 255), current_img[y:y+h, x:x+w])

    return current_img, change_detected