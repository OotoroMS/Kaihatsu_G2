import pygame
import queue
import threading
import SERIAL.serial_gate
# 定数(GUI)
from MAIN_OPRATION.GUI.Constants.screen_name import *
from MAIN_OPRATION.GUI.Constants.popup_name  import *
import MAIN_OPRATION.GUI.Managers.ScreenManager     as ScreenManager
import MAIN_OPRATION.GUI.Managers.PopupManager      as PopupManager
import MAIN_OPRATION.GUI.Managers.OperatingManager  as OperatingManager
SCREEN_SIZE = (1920, 1080)

class MainUIManager:
    def __init__(self, serial : SERIAL.serial_gate.SerialGate):
        self.screen = pygame.display.set_mode(SCREEN_SIZE, pygame.FULLSCREEN)
        # 各マネージャー
        # self.operation_manager  = OperatingManager(self.screen)
        self.screen_manager     = ScreenManager.ScreenManager(self.screen)
        self.popup_manager      = PopupManager.PopupManager(self.screen)
        self.operation_manager  = OperatingManager.OperatingManager(self.screen, serial)
        # 現在の画面
        self.curent_screen = MAIN
        self.running = True
        # 押しっぱなしフラグ
        self.is_hold_down = False
        self.hold_down_command = None
        # 更新頻度設定用
        self.clock = pygame.time.Clock()
        # 稼働状況保持用
        self.operation_status = ["エラー", "プログラムに問題があります"]
        self.error = ["エラー", "想定通りならこのメッセージは出ないはずだよ"]
    
    def run(self):
        while self.running:
            draw_result = self.screen_manager.screen_draw(self.curent_screen)
            self.operation_manager.status_receve_draw()
            popup_flg, popup_name, error = self.operation_manager.foward_error()
            if draw_result:
                self.check_event()
            if popup_flg:
                self.popup_manager.set_error_popup(error)
                self.show_popup(popup_name)
            # 画面更新
            pygame.display.update()
            self.clock.tick(15)
        return self.curent_screen

    # イベントを判別
    def check_event(self):
        event_result, is_click = self.screen_manager.screen_event_check(self.curent_screen)
        screen_result = self.screen_event(event_result, is_click)
    
    # 画面表示イベント
    def screen_event(self, event_result, is_click):
        if is_click and self.screen_manager.screen_search(event_result):
            self.curent_screen = event_result
            return True
        elif is_click and event_result == MOTION:
            self.curent_screen = event_result
            self.running = False
            return True
        if is_click and self.popup_manager.popup_search(event_result):
            self.show_popup(event_result)
            return True
        return False
    
    # ポップアップ表示
    def show_popup(self, popup_name):
        while True:
            self.popup_manager.popup_draw(popup_name)
            result, action = self.popup_manager.popup_event_check(popup_name)
            
            if result and popup_name == END_POPUP:
                self.running = False
                break
            elif action:
                break
            pygame.display.update()