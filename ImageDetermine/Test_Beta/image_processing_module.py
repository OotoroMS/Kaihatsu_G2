import cv2
import numpy as np
import os

class ImageProcessing:
    def __init__(self, crop_size, target_size):
        """
        :param crop_size: クロップする領域のサイズ (width, height)
        :param target_size: 画像を標準化する際の最終的なサイズ (width, height)
        """
        self.crop_size = crop_size
        self.target_size = target_size

    def crop_image(self, image, center=None):
        """
        画像を指定されたサイズにクロップする
        :param image: 入力画像
        :param center: クロップの中心位置 (x, y)。指定しない場合、画像の中心を使用。
        :return: クロップされた画像
        """
        height, width = image.shape[:2]
        crop_w, crop_h = self.crop_size
        
        if center is None:
            center = (width // 2, height // 2)
        
        x, y = center
        x1 = max(0, x - crop_w // 2)
        y1 = max(0, y - crop_h // 2)
        x2 = min(width, x + crop_w // 2)
        y2 = min(height, y + crop_h // 2)
        
        return image[y1:y2, x1:x2]

    def standardize_image(self, image):
        """
        画像を標準化（サイズ変更・正規化）する
        :param image: 入力画像
        :return: 標準化された画像
        """
        # サイズ変更
        standardized_image = cv2.resize(image, self.target_size)
        
        # 正規化（ピクセル値を0-1にスケール）
        standardized_image = standardized_image / 255.0
        
        return standardized_image

    def process_image(self, image_path):
        """
        画像をクロップし、標準化する
        :param image_path: 入力画像のパス
        :return: 処理済みの画像
        """
        image = cv2.imread(image_path)
        if image is None:
            raise FileNotFoundError(f"Image not found at path: {image_path}")
        
        cropped_image = self.crop_image(image)
        standardized_image = self.standardize_image(cropped_image)
        
        return standardized_image

if __name__ == "__main__":
    # サンプル画像を処理する例
    image_processor = ImageProcessing(crop_size=(200, 200), target_size=(128, 128))
    
    sample_image_path = './sample_image.jpg'
    if os.path.exists(sample_image_path):
        processed_image = image_processor.process_image(sample_image_path)
        
        # 処理結果を保存（確認用）
        output_path = './processed_image.jpg'
        cv2.imwrite(output_path, (processed_image * 255).astype(np.uint8))
        print(f"Processed image saved to {output_path}")
    else:
        print(f"Sample image not found at path: {sample_image_path}")