import pygame
# 定数
from GUI.constant.file_path                 import *
from GUI.constant.judge_result              import *
from GUI.constant.color                     import *
from GUI.constant.screen.motion_constant    import *
from GUI.constant.screen.screen_name        import *
from GUI.constant.popup.popup_name          import *
# 部品
from GUI.parts.Button   import Button
from GUI.parts.Picture  import Picture
# 基本クラス
from GUI.screen.BaseScreen  import BaseScreen

class MotitonScreen(BaseScreen):
    def __init__(self, screen: pygame.Surface) -> None:
        super().__init__(screen)

    # 画像を設定
    def setting_images(self):
        self.images = [
            Picture(self.screen, **TETLE_MOTION_STATUS),
            Picture(self.screen, **EXPTXT_TARGET_STATUS)
        ]
    
    # ボタンの設定
    def setting_buttons(self):
        self.buttons = [
            Button(self.screen, **BOTTON_BACK_STATUS,   func=self.back),
            Button(self.screen, **BUTTON_MOVE_STATUS,   func=self.move_move),
            Button(self.screen, **BUTTON_VISION_STATUS, func=self.move_vision),
            Button(self.screen, **RESET_BUTTON_STATUS, func=self.dbreset),
            Button(self.screen, **PASS_BUTTON_STATUS,  func=self.move_changepass)
        ]
    def draw(self):
        
        self.draw_images()
        self.draw_lines()
        self.draw_buttons()

    def draw_lines(self):
        pygame.draw.line(self.screen, **LINE_RED_STATUS)
        pygame.draw.line(self.screen, **LINE_BLUE_STATUS)

    # メイン画面に戻る
    def back(self):
        return MAIN, SUCCESS
    
    # 移動部に移動
    def move_move(self):
        return MOTION_MOVE, SUCCESS
    
    # 外観検査部に移動
    def move_vision(self):
        return MOTION_VITION, SUCCESS
    
    # パスワード変更画面に遷移
    def move_changepass(self):
        return MOTION_CHANGE, OK
    
    # データベース初期化
    def dbreset(self):
        return RESET_ASK, OK
