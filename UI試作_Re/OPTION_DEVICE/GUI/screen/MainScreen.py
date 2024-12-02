# メイン画面
import pygame
from typing import Tuple, Optional
# 定数
from GUI.constant.screen.screen_name    import *
from GUI.constant.screen.main_constant  import *
from GUI.constant.popup.popup_name      import *
from GUI.constant.judge_result          import *
# 部品
from GUI.parts.Button   import Button
from GUI.parts.Picture  import Picture
# 画面のベース
from GUI.screen.BaseScreen import BaseScreen

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