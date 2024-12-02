# スクリーンを制御するクラス
import pygame
# 定数
from GUI.constant.judge_result          import *
from GUI.constant.screen.screen_name    import *
# 暗転用モジュール
import GUI.parts.Blackout as Blackout
# 背景関係
from GUI.parts.Background   import *
# 各スクリーン
from GUI.screen.MainScreen          import MainScreen
from GUI.screen.PassScreen          import PassScreen
from GUI.screen.DataScreen          import DataScreen
from GUI.screen.CountScreen         import CountScreen
from GUI.screen.VisionScreen        import VisionScreen
from GUI.screen.MotionScreen        import MotitonScreen
from GUI.screen.MotionMoveScreen    import MotionMoveScreen
from GUI.screen.MotionVitionScreen  import MotionVitionScreen
from GUI.screen.ChangePassScreen    import ChangePassScreen
# シリアル通信用クラス

class ScreenManager:
    def __init__(self, screen : pygame.Surface) -> None:
        self.screen      = screen
        self.screen_now  = MAIN
        self.settng_screen()

    # 画面を登録
    def settng_screen(self):
        self.show_screens = {
            MAIN            : MainScreen(self.screen),
            PASS            : PassScreen(self.screen),
            DATA            : DataScreen(self.screen),
            DATA_COUNT      : CountScreen(self.screen),
            DATA_VISION     : VisionScreen(self.screen),
            MOTION          : MotitonScreen(self.screen),
            MOTION_MOVE     : MotionMoveScreen(self.screen, None),
            MOTION_VITION   : MotionVitionScreen(self.screen),
            MOTION_CHANGE   : ChangePassScreen(self.screen)
        }

    # 対応した画面を描画
    def screen_draw(self, key : str) -> bool:
        # スクリーンがあれば取得
        show_screen = self.screen_check(key)
        # 画面が切り替わっていなければ
        if show_screen and self.screen_now == key:
            backgrond = setting_backgrond(key)
            self.screen.blit(backgrond, ORIGEN)
            show_screen.draw()
            return SUCCESS
        # 切り替わっていれば
        elif show_screen:
            self.screen_blackout(key)
            self.screen_now = key
            return SUCCESS
        return FAILURE

    # キーに対応した画面があれば返し、なければNoneを返す
    def screen_check(self, key):
        if key in self.show_screens.keys():
            return self.show_screens[key]
        return None
    
    # 暗転して画面切り替え
    def screen_blackout(self, key):
        # 直前の画面と背景を読み込む
        past_background = setting_backgrond(self.screen_now)
        past_screen     = self.screen_check(self.screen_now)
        # 次の画面と背景を読み込む
        next_background = setting_backgrond(key)
        next_screen     = self.screen_check(key)
        # 暗転
        Blackout.brackout_screen(self.screen, past_background, past_screen.draw)
        # 明るくする処理
        Blackout.lightchenge_screen(self.screen, next_background, next_screen.draw)
    
    # クリック判定
    def screen_event_check(self, key):
        result = None
        normal = FAILURE
        check_screen = self.screen_check(key)
        if check_screen:
            result , normal = check_screen.click_event()
            return result, normal
        return result, normal

    # 渡されたキーが登録されているかを確認
    def screen_search(self, keys):
        if keys in self.show_screens.keys():
            return SUCCESS
        return FAILURE