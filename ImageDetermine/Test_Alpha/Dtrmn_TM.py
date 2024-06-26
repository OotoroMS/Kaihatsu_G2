### テンプレートマッチングで判別するプログラム ###
import cv2
import numpy as np

class TemplateMatching:
    def __init__(self, base_image_path):
        self.base_image = self.load_image(base_image_path)
        self.base_image_blur = self.preprocess_image(self.base_image)
    
    def load_image(self, file_path):
        image = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
        if image is None:
            raise ValueError(f"Image at path {file_path} could not be loaded.")
        return image

    def preprocess_image(self, image):
        blurred = cv2.GaussianBlur(image, (5, 5), 0)
        return blurred

    def match_template(self, check_image_path):
        check_image = self.load_image(check_image_path)
        check_image_blur = self.preprocess_image(check_image)
        
        result = cv2.matchTemplate(check_image_blur, self.base_image_blur, cv2.TM_CCOEFF_NORMED)
        threshold = 0.8
        loc = np.where(result < threshold)  # 一致度が低い箇所を検出
        
        return check_image, loc

    def draw_matches(self, image, loc, w, h):
        result_image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
        for pt in zip(*loc[::-1]):
            cv2.rectangle(result_image, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)
        return result_image

# メイン処理
def main(base_file_path, check_file_path):
    detector = TemplateMatching(base_file_path)
    check_image, loc = detector.match_template(check_file_path)
    w, h = detector.base_image.shape[::-1]
    result_image = detector.draw_matches(check_image, loc, w, h)

    # 結果を表示
    cv2.imshow('Detected Defects', result_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# テスト用
if __name__ == "__main__":
    base_file_path = 'path_to_base_image.jpg'  # 基準となる画像ファイルのパスを指定
    check_file_path = 'path_to_check_image.jpg'  # 検査する画像ファイルのパスを指定
    main(base_file_path, check_file_path)
