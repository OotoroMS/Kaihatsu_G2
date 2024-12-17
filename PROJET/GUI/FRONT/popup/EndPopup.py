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
from GUI.FRONT.constant.button    import BtnEnd
from GUI.FRONT.constant.text      import TextEnd

class EndPopup(BasePopup):
    def __init__(self, screen: pygame.Surface, to_back: Queue):
        super().__init__(screen, to_back)
    
    def setting_buttons(self):
        self.buttons = [
            Button(self.screen, BtnEnd.OK.pos, BtnEnd.OK.size,
                   BtnEnd.OK.path, self.ok_func),
            Button(self.screen, BtnEnd.NG.pos, BtnEnd.NG.size,
                   BtnEnd.NG.path, self.ng_func)
        ]
    
    def setting_texts(self):
        self.texts = [
            Text(self.screen, TextEnd.End.pos, TextEnd.End.text,
                 TextEnd.End.color, self.text_font)
        ]
    
    def ok_func(self):
        print("終了します")
        self.to_back.put("End")
    
    def ng_func(self):
        print("ベース画面に戻ります")
        self.to_back.put("NG")