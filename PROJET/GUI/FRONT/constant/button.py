# GUI/FRONT/constant/button.py

from enum import Enum

# 自作プログラムをimport
# 定数ファイル
from GUI.FRONT.constant.file_path import BUTTON_FILE_PATH

class ButtonBase(Enum):
    # 共通のボタン設定（親クラス）
    def __init__(self, pos, size, path):        
        self.pos = pos              # ボタンの座標
        self.size = size            # ボタンのサイズ
        self.path = path  # 画像パス

class BtnBase(ButtonBase):
    # BaseScreenで使用するボタンたち
    Main = ((1000, 300), (700, 350),
            BUTTON_FILE_PATH + "button_motion.png")
    End  = ((0, 960), (330, 120), 
            BUTTON_FILE_PATH + "button_end.png")
    # BasePopupで使用するボタンたち
#     OK   = None
#     NG   = None

class BtnMain(ButtonBase):
    # MainScreenで使用するボタンたち    
    Back = ((0, 960), (330, 120), 
            BUTTON_FILE_PATH + "button_back.png")