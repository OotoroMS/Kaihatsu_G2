# GUI/FRONT/popup/EndPopup.py

# デバック用
import sys
import os
sys.path.append(os.getcwd())

import pygame
from queue import Queue
from typing import Tuple, Optional

# 自作プログラムをimport
from GUI.FRONT.parts.Button import Button
from GUI.FRONT.parts.Text   import Text
from GUI.FRONT.popup.BasePopup import BasePopup
# 定数ファイル
from GUI.FRONT.constant.file_path import FONT
from GUI.FRONT.constant.color     import GRAY, BLACK
from GUI.FRONT.constant.button    import BtnMeasure
from GUI.FRONT.constant.text      import TextMeasure

class MeasurePopup(BasePopup):
    def __init__(self, screen: pygame.Surface, to_back: Queue):
        super().__init__(screen, to_back)
    
    def setting_buttons(self):
        self.buttons = [
            Button(self.screen, BtnMeasure.OK.pos, BtnMeasure.OK.size,
                   BtnMeasure.OK.path, self.ok_func),
        ]
    
    def setting_texts(self):
        self.texts = [
            Text(self.screen, TextMeasure.View.pos, 
                 TextMeasure.View.text,
                 TextMeasure.View.color, self.text_font)
        ]
    
    def ok_func(self):
        print("測定結果を表示しました")
        self.to_back.put("NG")