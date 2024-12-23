import pygame
# 背景管理
import GUI.parts.Background as Background
# 定数
from GUI.constants.screen_name  import *
# 各画面のクラス
from GUI.screens.ChangePassScreen   import ChangePassScreen
from GUI.screens.SelectScreen       import SelectScreen
from GUI.screens.VisionScreen       import VitisonScreen
from GUI.screens.MoveScreen         import MoveScreen
# 暗転処理
import GUI.parts.Blackout   as  Blackout


class ScreenManager:
    def __init__(self, screen : pygame.Surface) -> None:
        self.screen      = screen
        self.screen_now  = MAIN
        self.settng_screen()

    # 画面を登録
    def settng_screen(self):
        self.show_screens = {
            MAIN    : SelectScreen(self.screen),
            VISION  : VitisonScreen(self.screen),
            MOVE    : MoveScreen(self.screen),
            CHANGE  : ChangePassScreen(self.screen)
        }
    
    def screen_draw(self, key : str) -> bool:
        show_screen = self.screen_check(key)
        if key == self.screen_now:
            background = Background.setting_backgrond(key)
            self.screen.blit(background, Background.ORIGEN)
            show_screen.draw()
            return True
        elif show_screen:
            # 暗転
            screen     = self.screen_check(self.screen_now)
            background = Background.setting_backgrond(self.screen_now)
            Blackout.brackout_screen(self.screen, background, screen.draw)
            # 暗転解除
            background = Background.setting_backgrond(key)
            Blackout.lightchenge_screen(self.screen, background, show_screen.draw)
            return True
        return False

    def screen_event_check(self, key : str):
        result = None
        normal = False
        check_screen = self.screen_check(key)
        if check_screen:
            result , normal = check_screen.click_event()
            return result, normal
        return result, normal
    
    # キーに対応した画面があれば返し、なければNoneを返す
    def screen_check(self, key):
        if key in self.show_screens.keys():
            return self.show_screens[key]
        return None
    
    # 渡されたキーが登録されているかを確認
    def screen_search(self, keys):
        if keys in self.show_screens.keys():
            return True
        return False
    
    def screen_lamp_update_yellow(self, key):
        check_screen = self.screen_check(self.screen_now)
        if hasattr(check_screen, "lamp_update_yellow"):
            check_screen.lamp_update_yellow(key)

    def screen_lamp_update_green(self, key):
        check_screen = self.screen_check(self.screen_now)
        if hasattr(check_screen, "lamp_update_green"):
            check_screen.lamp_update_green(key)
    
    def move_lamp_update(self, opration, command):
        check_screen = self.screen_check(self.screen_now)
        if hasattr(check_screen, "move_lamp_update"):
            check_screen.move_lamp_update(opration, command)
