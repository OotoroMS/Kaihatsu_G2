import os
import cv2
import numpy as np
from ultralytics import YOLO

class DeepLearning:
    # コンストラクタ
    def __init__(self):
        # YOLOv5の初期化
        self.yolo = YOLO("yolov5su.pt")  # 新しいモデルファイル名を使用

    # ディープラーニングで判別
    def determine(self, img):
        # グレースケール画像を3チャンネルに変換
        if len(img.shape) == 2:
            img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
        
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
                top_left_corner = (box[0], box[1] - label_size[1] - base_line)
                bottom_right_corner = (box[0] + label_size[0], box[1])
                cv2.rectangle(img, top_left_corner, bottom_right_corner, (0, 255, 0), cv2.FILLED)
                cv2.putText(img, class_name, (box[0], box[1] - base_line), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 0), 2)

        # 画像を表示
        cv2.imshow("Result", img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        # 結果を返す
        return results
    
# メイン処理
def main():
    dl = DeepLearning()
    cap = cv2.VideoCapture(0)
    ret, current_image = cap.read()
    dl.determine(current_image)

if __name__ == "__main__":
    main()
