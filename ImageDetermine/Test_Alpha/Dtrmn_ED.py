import cv2
import numpy as np
import os

class EdgeDetection:
    def __init__(self, ksize=3, scale=1, delta=0, threshold=50, blur_ksize=11):
        self.ksize = ksize
        self.scale = scale
        self.delta = delta
        self.threshold = threshold
        self.blur_ksize = blur_ksize

    def detect_edges(self, image):
        """
        ラプラシアンフィルタを使用してエッジを検出
        """
        # グレースケール画像を反転
        inverted_image = cv2.bitwise_not(image)
        cv2.imshow('Inverted Image', inverted_image)
        
        # 平滑化を強化
        blurred = cv2.GaussianBlur(inverted_image, (self.blur_ksize, self.blur_ksize), 0)
        cv2.imshow('Blurred Image', blurred)
        
        # ヒストグラム平坦化
        equalized = cv2.equalizeHist(blurred)
        cv2.imshow('Equalized Image', equalized)
        
        # ラプラシアンフィルタでエッジ検出
        laplacian = cv2.Laplacian(equalized, cv2.CV_16S, ksize=self.ksize, scale=self.scale, delta=self.delta)
        abs_laplacian = cv2.convertScaleAbs(laplacian)
        cv2.imshow('Laplacian Image', abs_laplacian)

        # 二値化でエッジを強調
        _, binary_edges = cv2.threshold(abs_laplacian, self.threshold, 255, cv2.THRESH_BINARY)
        return binary_edges

    def find_defects(self, image):
        """
        エッジ検出と傷の輪郭を見つける
        """
        # グレースケール画像を反転
        inverted_image = cv2.bitwise_not(image)
        cv2.imshow('Inverted Image for Defects', inverted_image)
        
        # 平滑化を強化
        blurred = cv2.GaussianBlur(inverted_image, (self.blur_ksize, self.blur_ksize), 0)
        cv2.imshow('Blurred Image for Defects', blurred)
        
        # ヒストグラム平坦化
        equalized = cv2.equalizeHist(blurred)
        cv2.imshow('Equalized Image for Defects', equalized)
        
        # エッジ検出
        edges = self.detect_edges(equalized)
        
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
        """
        元の画像に傷の輪郭を描画
        """
        result = cv2.drawContours(image.copy(), defects, -1, (0, 255, 0), 2)
        return result

def main():
    # カレントディレクトリを取得
    current_dir = os.getcwd()
    print(f"Current Directory: {current_dir}")

    # サンプル画像のパスを設定
    image_path = os.path.join(current_dir, 'ImageDetermine/Test_Alpha/Images', 'SMPL_Dmg.JPG')
    
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
            edge_detector = EdgeDetection(ksize=3, scale=1, delta=0, threshold=20, blur_ksize=11)
            
            # 傷の検出
            defects = edge_detector.find_defects(image)
            
            # 傷の描画
            result_image = edge_detector.draw_defects(image, defects)
            
            # 結果の表示
            cv2.imshow('Detected Defects', result_image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
