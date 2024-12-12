# GUI/FRONT/constant/background.py

from enum import Enum
import pygame

# 自作プログラムをimport
# 定数ファイル
from GUI.FRONT.constant.file_path import BACKGROUND_FILE_PATH

class BackGroundBase(Enum):
    # 共通のボタン設定（親クラス）
    def __init__(self, path):
        self.path = path  # 画像パス
        self.img = pygame.image.load(self.path)  # 画像を読み込む

    def scale_to_window(self, screen: pygame.Surface):
        """スクリーンのサイズに合わせて画像をスケーリング"""
        window_width, window_height = screen.get_size()  # ウィンドウサイズを取得
        self.img = pygame.transform.scale(self.img, (window_width, window_height))  # スケーリング

    def draw(self, screen: pygame.Surface):
        """指定したスクリーンに背景画像を描画"""
        screen.blit(self.img, (0, 0))  # (0, 0)は画像をスクリーン左上に配置

class BackBase(BackGroundBase):
    Base = BACKGROUND_FILE_PATH + "base.jpg"  # 背景画像のパス

class BackMain(BackGroundBase):
    Main = BACKGROUND_FILE_PATH + "password.jpg"  # 背景画像のパス
