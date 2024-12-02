# UI全体の制御を行うプログラム
import pygame
from SERIAL.pc_comands  import *
# 定数
from GUI.constant.color                 import *
from GUI.constant.judge_result          import *
from GUI.constant.operating_status      import *
from GUI.constant.screen.screen_name    import *
from GUI.constant.popup.popup_name      import *
# 各マネージャー
from GUI.manager.ScreenManager      import ScreenManager
from GUI.manager.PopupManager       import PopupManager
from GUI.manager.OperatingManager   import OperatingManager

FPS = 15

class Application:
    def  __init__(self, screen : pygame.Surface, serial : PCManager) -> None:
        self.screen            = screen
        self.serial            = serial
        self.is_ranning        = True
        self.current_screen    = MAIN
        self.flag_popup        = False                # ポップアップの描画フラグ
        self.view_popup        = ""                   # 表示するポップアップ
        self.error             = None
        self.screen_manager    = ScreenManager(self.screen)
        self.popup_manager     = PopupManager(self.screen)
        self.operating_manager = OperatingManager(self.screen, self.serial)
        self.clock             = pygame.time.Clock()

        self.tcnt = 15   # デバック用
    
    def run(self):
        while self.is_ranning:
            self.show_popup()
            draw_result = self.screen_manager.screen_draw(self.current_screen)
            self.operating_manager.status_receve_draw(self.tcnt)
            if draw_result:
                self.check_event()
            pygame.display.update()
            self.clock.tick(FPS)
            # デバック用
            if self.tcnt >= 15:
                self.tcnt = 0
            else:
                self.tcnt += 1

    def check_event(self):
        event_result, normal = self.screen_manager.screen_event_check(self.current_screen)
        if normal and self.screen_manager.screen_search(event_result):
            self.screen_update(event_result)
        elif normal and self.popup_manager.popup_search(event_result):
            self.flag_popup = True
            self.view_popup = event_result

    def screen_update(self, event :str):
        status = self.operating_manager.operating_status
        if event == PASS and status != STATUS_STOP:
            self.flag_popup = True
            self.view_popup = STOP_POPUP
        else:
            self.current_screen = event

    # POPUP表示
    def show_popup(self):
        while self.flag_popup:
            self.popup_manager.popup_draw(self.view_popup)
            event_result, normal = self.popup_manager.popup_event_check(self.view_popup)
            # event_resultには表示するポップアップが入っている
            # エラーが発生した際はnormalがFalseになる
            if event_result and normal:
                self.flag_popup, self.view_popup = self.next_screen()                
            # 終了確認画面の戻るを検知する用
            elif normal:
                self.flag_popup = None
                self.error      = None
                self.view_popup = ""
            pygame.display.update()
    
    def next_screen(self):
        # 各ポップアップが表示された時に行う動作の分岐        
        if self.view_popup == END_POPUP:
            self.is_ranning = False
        elif self.view_popup == SPASS_POPUP:
            self.current_screen = MOTION
        elif self.view_popup == RESET_ASK:
            return True, DB_RESET
        return False, ""