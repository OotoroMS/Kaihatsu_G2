# UI全体の制御を行うプログラム
import pygame
# デバック用
import sys
import os
sys.path.append(os.getcwd())
#sys.path.append("../MAIN_DEVICE")
# 自作プログラムをインポート
from SERIAL.pc_comands          import *
from GUI.constant.color         import *
from GUI.constant.popup_message import *
from GUI.constant.screen_name   import *
from GUI.constant.popup_name    import *
from GUI.parts.ScreenManager    import ScreenManager

TRUE   = True
FALSE  = False
FPS = 15
class Application:
    # screen : pygameのスクリーン(Sarface), serial : 制作したシリアル通信用クラス
    def __init__(self, screen : pygame.Surface, serial : PCManager) -> None:
        self.screen          = screen
        self.serial          = serial
        self.running         = TRUE                 # ループ管理変数
        self.current_screen  = MAIN                 # 現在の描画画面
        self.previous_screen = self.current_screen  # 前回の描画画面
        self.flag_popup      = FALSE                # ポップアップの描画フラグ
        self.view_popup      = END                  # 表示するポップアップ
        self.screen_manager  = ScreenManager(self.screen, self.serial)
        self.clock = pygame.time.Clock()
        self.clock.tick(FPS)

    def check_event(self):
        event_result, normal = self.screen_manager.screen_event_check(self.current_screen)
        if normal and self.screen_manager.screen_search(event_result):
            self.current_screen = event_result
        if event_result == END:
            self.running = False
    
    def ran(self):
        while self.running:
            self.clock.tick(15)
            draw_result = self.screen_manager.screen_draw(self.current_screen)
            if draw_result:
                self.check_event()
            else:
                print("curent_screenの値に問題があります")
                self.running - False
            pygame.display.update()

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((1920,1080))
    app = Application(screen, None)
    app.ran()
    pygame.quit()