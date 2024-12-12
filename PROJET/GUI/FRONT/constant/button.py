# GUI/FRONT/constant/button.py

# 各ボタンの設定をまとめたファイル
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
    OK   = ((1000, 300), (330, 120),
            BUTTON_FILE_PATH + "pic76.png")
    NG   = ((1000, 500), (330, 120),
            BUTTON_FILE_PATH + "pic77.png")

class BtnMain(ButtonBase):
    # MainScreenで使用するボタンたち    
    Back = ((0, 960), (330, 120), 
            BUTTON_FILE_PATH + "button_back.png")

class BtnEnd(ButtonBase):
    # EndPopupで使用するボタンたち
    OK   = ((400, 700), (340, 150),
            BUTTON_FILE_PATH + "pic76.png")
    NG   = ((1200, 700), (340, 150),
            BUTTON_FILE_PATH + "pic77.png")

class BtnOrignReset(ButtonBase):
    # OriginResetPopupで使用するボタンたち
    OK   = ((400, 700), (340, 150),
            BUTTON_FILE_PATH + "pic76.png")
    NG   = ((1200, 700), (340, 150),
            BUTTON_FILE_PATH + "pic77.png")

class BtnMeasure(ButtonBase):
    OK   = ((800, 700), (340, 150),
            BUTTON_FILE_PATH + "pic76.png")