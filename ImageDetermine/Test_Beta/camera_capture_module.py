import cv2
import time
import os

class CameraCapture:
    def __init__(self, resolution=(2592, 1944), save_directory='./CapturedImages'):
        self.resolution = resolution
        self.save_directory = save_directory
        self.camera = None
        
        # 保存先ディレクトリが存在しない場合、作成する
        if not os.path.exists(self.save_directory):
            os.makedirs(self.save_directory)

    def initialize_camera(self, camera_index=0):
        """
        カメラを初期化し、指定された解像度に設定する
        """
        self.camera = cv2.VideoCapture(camera_index)
        if not self.camera.isOpened():
            raise RuntimeError(f"Camera with index {camera_index} could not be opened.")
        
        # 解像度の設定
        self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, self.resolution[0])
        self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, self.resolution[1])

    def capture_image(self, filename_prefix='image', delay=0):
        """
        画像を撮影し、指定されたフォルダに保存する
        :param filename_prefix: 保存される画像ファイル名の接頭辞
        :param delay: 撮影前の待機時間（秒）
        """
        if delay > 0:
            time.sleep(delay)
        
        ret, frame = self.camera.read()
        if not ret:
            raise RuntimeError("Failed to capture image from camera.")
        
        # ファイル名の生成
        timestamp = time.strftime('%Y%m%d_%H%M%S')
        filename = f"{filename_prefix}_{timestamp}.jpg"
        filepath = os.path.join(self.save_directory, filename)
        
        # 画像の保存
        cv2.imwrite(filepath, frame)
        print(f"Image saved to {filepath}")

    def release_camera(self):
        """
        カメラを解放する
        """
        if self.camera:
            self.camera.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    try:
        # 撮影モジュールのインスタンス作成
        camera_capture = CameraCapture(save_directory='./CapturedImages')
        
        # カメラの初期化
        camera_capture.initialize_camera()
        
        # 画像を撮影
        camera_capture.capture_image(filename_prefix='inspection_image', delay=2)
        
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # カメラの解放
        camera_capture.release_camera()