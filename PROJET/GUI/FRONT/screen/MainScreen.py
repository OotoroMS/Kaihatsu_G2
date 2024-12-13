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
            Button(self.screen, BtnMain.End.pos, BtnMain.End.size,
                   BtnMain.End.path, self.end_func)
        ]
    
    def end_func(self):
        print("終了ポップアップへ")
        self.to_back.put("EndPopup")