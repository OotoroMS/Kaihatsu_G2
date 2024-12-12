# GUI/FRONT/screen/MainScreen.py

# デバック用
import sys
import os
sys.path.append(os.getcwd())

import pygame
from queue import Queue
from typing import Tuple, Optional

# 自作プログラムをimport
from GUI.FRONT.screen.BaseScreen import BaseScreen
from GUI.FRONT.parts.Button import Button
# 定数ファイル
from GUI.FRONT.constant.button import BtnMain
from GUI.FRONT.constant.background import BackMain

class MainScreen(BaseScreen):
    def __init__(self, screen: pygame.Surface, to_back: Queue):
        super().__init__(screen, to_back)
        self.background = BackMain.Main
    
    def setting_images(self):
        self.images = []
    
    def setting_buttons(self):
        self.buttons = [
            Button(self.screen, BtnMain.Back.pos, BtnMain.Back.size,
                   BtnMain.Back.path, self.func)
        ]
    
    def func(self):
        print("メイン画面のボタンが押されました")
        self.to_back.put("BaseScreen")