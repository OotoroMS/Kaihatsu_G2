# UI全体の制御を行うプログラム
import pygame
# デバック用
import sys
sys.path.append("../MAIN_DEVICE")
# 自作プログラムをインポート
from SERIAL.manager.SerialUIBridge  import SerialUIBridge
from DEGITALINDICATOR.Meas          import MeasurementConverter
from GUI.constant.color             import *
from GUI.constant.popup_message     import *
from GUI.constant.screen_name       import *
from GUI.constant.popup_name        import *
from GUI.constant.operating_status  import *
# 各マネージャー
from GUI.manager.ScreenManager    import ScreenManager
from GUI.manager.PopupManager     import PopupManager
from GUI.manager.OperatingManager import OperatingManager
TRUE   = True
FALSE  = False
FPS = 15
class Application:
    # screen : pygameのスクリーン(Sarface), serial : 制作したシリアル通信用クラス
    def __init__(self, screen : pygame.Surface, serial : SerialUIBridge) -> None:
        self.screen            = screen
        self.serial            = serial
        self.running           = TRUE                 # ループ管理変数
        self.current_screen    = MAIN                 # 現在の描画画面
        self.previous_screen   = self.current_screen  # 前回の描画画面
        self.flag_popup        = FALSE                # ポップアップの描画フラグ
        self.view_popup        = ""                   # 表示するポップアップ
        self.error             = None
        self.screen_manager    = ScreenManager(self.screen, self.serial)
        self.popup_manager     = PopupManager(self.screen)
        self.operating_manager = OperatingManager(self.screen, self.serial)
        self.clock = pygame.time.Clock()
        self.clock.tick(FPS)
        
        self.tcnt = 15   # デバック用

    def check_event(self):
        event_result, normal = self.screen_manager.screen_event_check(self.current_screen)
        # 判別
        if normal and self.screen_manager.screen_search(event_result):
            if event_result ==  PASS and self.operating_manager.operating_status == STATUS_ACTIVE:
                self.flag_popup = TRUE
                self.view_popup = ACTIVE_PASS
            else:
                self.current_screen = event_result
        elif normal and self.popup_manager.popup_search(event_result):
            self.flag_popup = TRUE
            self.view_popup = event_result    

    # POPUP表示
    def show_popup(self):
        if self.view_popup == ERROR_POPUP:
                self.popup_manager.set_error_popup(self.error)
                self.operating_manager.status_check()
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
                self.view_popup = ""
                self.error      = None
            pygame.display.update()

    def next_screen(self):
        # 各ポップアップが表示された時に行う動作の分岐        
        if self.view_popup == END_POPUP:
            self.running = False
        elif self.view_popup == SPASS_POPUP:
            self.current_screen = MOTION            
        elif self.view_popup == RESET_ASK:
            return True, DB_RESET
        elif self.view_popup == INDICATOR_OK:
            self.current_screen = MEAS
        return None, ""

    def ran(self):
        while self.running:  
            self.show_popup()
            draw_result = self.screen_manager.screen_draw(self.current_screen)
            self.operating_manager.status_receve_draw(self.tcnt)
            self.flag_popup, self.view_popup, self.error = self.operating_manager.foward_error()
            if draw_result:
                self.check_event()
            else:
                print("curent_screenの値に問題があります")
                self.running - False
            pygame.display.update()
            self.clock.tick(FPS)
            # デバック用
            if self.tcnt >= 15:
                self.tcnt = 0
            else:
                self.tcnt += 1

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((1920,1080))
    app = Application(screen, None)
    app.ran()
    pygame.quit()