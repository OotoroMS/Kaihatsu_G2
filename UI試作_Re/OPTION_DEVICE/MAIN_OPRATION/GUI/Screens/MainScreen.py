# メイン画面
import pygame
from typing import Tuple, Optional
# 定数
from MAIN_OPRATION.GUI.Constants.screen_name    import *
from MAIN_OPRATION.GUI.Constants.popup_name     import *
from MAIN_OPRATION.GUI.Constants.main_constant  import *
from MAIN_OPRATION.GUI.Constants.judge_result   import *
# 部品
from MAIN_OPRATION.GUI.Parts.Button   import Button
from MAIN_OPRATION.GUI.Parts.Picture  import Picture
# 画面のベース
from MAIN_OPRATION.GUI.Screens.BaseScreen import BaseScreen

class MainScreen(BaseScreen):
    def __init__(self, screen: pygame.Surface) -> None:
        super().__init__(screen)
    
    # 画像を設定
    def setting_images(self):
        self.images = [
            Picture(self.screen, **MAIN_TETLE_STATUS),
            Picture(self.screen, **EXPTXT_DATA_STATUS),
            Picture(self.screen, **EXPTXT_MOTION_STATUS)
        ]
    
    # ボタンを設定
    def setting_buttons(self):
        self.buttons = [
            Button(self.screen, **BUTTON_END_STATUS,    func=self.end),
            Button(self.screen, **BUTTON_DATA_STATUS,   func=self.move_data),
            Button(self.screen, **BUTTON_MOTION_STATUS, func=self.move_motion)
        ]
    
    # 終了
    def end(self):
        return END_POPUP, SUCCESS
    
    # データ一覧画面に遷移
    def move_data(self):
        return DATA, SUCCESS
    
    def move_motion(self):
        return PASS, SUCCESS