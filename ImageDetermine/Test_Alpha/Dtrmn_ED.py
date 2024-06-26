import cv2
import numpy as np
import os

class EdgeDetection:
    def __init__(self, threshold1=50, threshold2=150):
        self.threshold1 = threshold1
        self.threshold2 = threshold2

    def detect_edges(self, image):
        # エッジ検出を実行
        edges = cv2.Canny(image, self.threshold1, self.threshold2)
        return edges

    def find_defects(self, image):
        # エッジ検出
        edges = self.detect_edges(image)
        
        # 輪郭を見つける
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        defects = []
        for contour in contours:
            # 面積が一定以上の輪郭を傷と見なす
            area = cv2.contourArea(contour)
            if area > 100:  # この閾値は調整が必要
                defects.append(contour)

        return defects

    def draw_defects(self, image, defects):
        # 元の画像に傷の輪郭を描画
        result = cv2.drawContours(image.copy(), defects, -1, (0, 255, 0), 2)
        return result

# テストコード（実際のメインプログラムでは別途呼び出し）
if __name__ == "__main__":
    # カレントディレクトリを確認
    current_dir = os.getcwd()
    print(f"Current Directory: {current_dir}")
    
    # サンプル画像のパスを設定
    image_path = os.path.join(current_dir, 'ImageDetermine', 'Test_Alpha', 'Images', 'SMPL_NoDmg.JPG')
    
    # ファイルが存在するかを確認
    if not os.path.exists(image_path):
        print(f"Error: File '{image_path}' does not exist.")
    else:
        # サンプル画像を読み込み（ここでは赤外線カメラのグレースケール画像を想定）
        image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

        if image is None:
            print(f"Error: Unable to load image '{image_path}'.")
        else:
            # サンプル画像を表示
            cv2.imshow('Original Image', image)
            
            # エッジ検出器の初期化
            edge_detector = EdgeDetection()
            
            # 傷の検出
            defects = edge_detector.find_defects(image)
            
            # 傷の描画
            result_image = edge_detector.draw_defects(image, defects)
            
            # 結果の表示
            cv2.imshow('Detected Defects', result_image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
