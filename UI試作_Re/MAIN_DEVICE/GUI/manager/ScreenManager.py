# スクリーンを制御するクラス
import pygame
import sys
sys.path.append("../MAIN_DEVICE")
# 暗転用モジュール
import GUI.parts.Blackout        as Blackout
# 測定用
from DEGITALINDICATOR.Meas       import MeasurementConverter
# 定数
from GUI.constant.screen_name    import *
# 背景関係モジュール
from GUI.parts.Background        import *
# 各スクリーンのクラス
from GUI.screen.MainScreen       import MainScreen
from GUI.screen.PassScreen       import PassScreen
from GUI.screen.DataScreen       import DataScreen
from GUI.screen.CountScreen      import CountScreen
from GUI.screen.GraphScreen      import GraphScreen
from GUI.screen.MotionScreen     import MotionScreen
from GUI.screen.MoveScreen       import MoveScreen
from GUI.screen.WashScreen       import WashScreen
from GUI.screen.MeasScreen       import MeasScreen
from GUI.screen.StackScreen      import StackScreen
from GUI.screen.ChangePassScreen import ChangePassScreen
from GUI.screen.ChangeMeasScreen import ChangeMeasScreen
# シリアル通信クラス
from SERIAL.manager.SerialUIBridge  import SerialUIBridge

SACSESS = True
FAILD   = False
ORIGEN  = (0,0)
class ScreenManager:
    def __init__(self, screen : pygame.Surface, serial : SerialUIBridge) -> None:
        self.screen       = screen
        self.view_screens = {
            MAIN        : MainScreen(self.screen),
            PASS        : PassScreen(self.screen),
            DATA        : DataScreen(self.screen),
            COUNT       : CountScreen(self.screen),
            GRAPH       : GraphScreen(self.screen),
            MOTION      : MotionScreen(self.screen),
            MOVE        : MoveScreen(self.screen, serial),
            WASH        : WashScreen(self.screen, serial),
            MEAS        : MeasScreen(self.screen, serial),
            STOCK       : StackScreen(self.screen, serial),
            CHANGE      : ChangePassScreen(self.screen),
            CHANGE_MEAS : ChangeMeasScreen(self.screen)
        }
        self.screen_now  = MAIN
        self.screen_past = self.screen_now
    
    # 対応した画面があれば描画
    def screen_draw(self, curent_screen : str):
        screen = self.screen_check(curent_screen)
        if screen and self.screen_now != curent_screen:     # 画面遷移時
            self.screen_blackout(curent_screen)
            self.screen_past_check(curent_screen)
            return SACSESS
        elif screen:
            background = setting_backgrond(curent_screen)   # 通常時
            self.screen.blit(background, ORIGEN)
            screen.draw()
            self.screen_past_check(curent_screen)
            return SACSESS
        return FAILD

    # 前回の描画画面と今回の描画画面を比較し、違った場合は保持する。
    def screen_past_check(self, screen):
        if self.screen_now != screen:
            self.screen_past = self.screen_now
        self.screen_now = screen

    # 画面切り替え処理
    def screen_blackout(self, cureent_screen):
        # 暗転処理
        background = setting_backgrond(self.screen_now)
        screen     = self.screen_check(self.screen_now)
        Blackout.brackout_screen(self.screen, background, screen.draw)
        # 明るくする処理
        background = setting_backgrond(cureent_screen)
        screen     = self.screen_check(cureent_screen)
        Blackout.lightchenge_screen(self.screen, background, screen.draw)

    # 画面が登録されているか確認
    def screen_check(self, keys):
        if keys in self.view_screens.keys():
            return self.view_screens[keys]
        return None

    # クリックイベントが発生したか確認
    def screen_event_check(self, curent_screen : str):
        result = None
        normal = FAILD
        screen = self.screen_check(curent_screen)
        if screen:
            result, normal = screen.click_event()
            return result, normal
        return result, normal
    
    # 渡されたキーが登録されているかを確認
    def screen_search(self, keys):
        if keys in self.view_screens.keys():
            return True
        return False 