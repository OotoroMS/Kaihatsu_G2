import argparse
import os
import numpy as np
from image_processing_module import ImageProcessing
from model_handler_module import ModelHandler
from camera_capture_module import CameraCapture
from rotation_control_module import RotationControl

# 定数設定
CROP_SIZE = (2112, 640)
TARGET_SIZE = (2112, 640)
INPUT_SHAPE = (2112, 640, 1)
CAMERA_RESOLUTION = (2592, 1944)
SAVE_DIRECTORY = './CapturedImages'
ROTATION_PORT = 'COM3'
BAUDRATE = 9600
TRAINING_IMAGE_COUNT = 360//14
ROTATE_COMMAND_TRAIN = 'ROTATE_CW_14'
ROTATE_COMMAND_INSPECT = 'ROTATE_CW_45'
INSPECTION_COUNT = 10


def main():
    parser = argparse.ArgumentParser(description="Image Inspection System")
    parser.add_argument('--mode', type=str, choices=['train', 'inspect'], required=True, help="Mode of operation: 'train' or 'inspect'")
    args = parser.parse_args()
    
    # 共通設定
    image_processor = ImageProcessing(crop_size=CROP_SIZE, target_size=TARGET_SIZE)
    model_handler = ModelHandler(input_shape=INPUT_SHAPE)
    camera = CameraCapture(resolution=CAMERA_RESOLUTION, save_directory=SAVE_DIRECTORY)
    rotation_control = RotationControl(port=ROTATION_PORT, baudrate=BAUDRATE)

    if args.mode == 'train':
        # トレーニングモード
        print("Starting training mode...")
        camera.initialize_camera()
        training_images = []
        
        for i in range(TRAINING_IMAGE_COUNT):  # 任意の回数分の撮影
            rotation_control.send_rotation_command(ROTATE_COMMAND_TRAIN)  # 少しずつ回転しながら撮影
            camera.capture_image(filename_prefix=f'training_image_{i}', delay=1)
            image_path = f'{SAVE_DIRECTORY}/training_image_{i}.jpg'
            processed_image = image_processor.process_image(image_path)
            training_images.append(processed_image)
        
        camera.release_camera()
        training_images = np.array(training_images)
        model_handler.train_model(train_data=training_images, epochs=10)
    
    elif args.mode == 'inspect':
        # 検査モード
        print("Starting inspection mode...")
        model_handler.load_model()
        camera.initialize_camera()
        
        for i in range(INSPECTION_COUNT):  # 任意の回数分の検査
            rotation_control.send_rotation_command(ROTATE_COMMAND_INSPECT)  # 回転して検査
            camera.capture_image(filename_prefix=f'inspection_image_{i}', delay=1)
            image_path = f'{SAVE_DIRECTORY}/inspection_image_{i}.jpg'
            processed_image = image_processor.process_image(image_path)
            reconstructed_image = model_handler.predict(processed_image)
            
            # 検査結果の表示（簡易的に再構成画像との差異を計算）
            diff = np.abs(processed_image - reconstructed_image).mean()
            print(f"Inspection {i}: Difference from original image = {diff}")
        
        camera.release_camera()

if __name__ == "__main__":
    main()