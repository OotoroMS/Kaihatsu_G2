# 画面の設定を置いておく場所
# 画面サイズ  1024x600
import pygame
import parts.Vital as Vital
# 自作のクラス
# 定数
from constant.FilePath   import *
from constant.ScreenName import *
from constant.PopupName  import *
# 画面描画・処理クラス
from screen.MainScreen       import MainFrame
from screen.DataScreen       import DataFrame
from screen.PassScreen       import PassFrame
from screen.GraphScreen      import GraphFrame
from screen.CountScreen      import CountFrame
from screen.MotionTestScreen import MotionTestFrame
from screen.Test01Screen     import Test01Frame
from screen.Test02Screen     import Test02Frame
from screen.ChangePassScreen import ChangePassScreen
# ポップアップ描画・処理クラス
from popup.BasePopup        import BasePopup
from popup.EndPopup         import EndPopup
from popup.WarningPopup     import WorningPopup
from popup.PassErrorPopup   import PassErrorPopup
from popup.ErrorPopup       import ErrorPopup
from popup.DBresetPopup     import DBresetPopup
# 暗転処理
import parts.Blackout as BlackOut

# カラーコード
BLACK = ((0,0,0))
GRAY  = ((200,200,200))
# 画面更新処理
FPS = 60
# 背景画像
BACKGROUNDIMAGE = {
    "main"       : BACKGROUNDFILEPATH + "back01.jpg",
    "pass"       : BACKGROUNDFILEPATH + "back02.jpg",
    "motiontest" : BACKGROUNDFILEPATH + "back01.jpg",
    UPDATE_PASS  : BACKGROUNDFILEPATH + "back02.jpg"
}
# 初期画面
FARSTSCREEN    = "main" 
# POPUPテキスト
NONEPASSTEXT     = "パスワードを入力してください"
CHANGEPASSTEXT   = "パスワードを変更しました"
NO_DATA_TEXT     = "データベースにデータが存在しません"
DB_RESET_TEXT    = "データベースをリセットしました"
# 試験用(本実装時には削除推奨)
FARSTVITAL     = "停止中"
class App:
    #   screen : pygameのスクリーン,font : 日本語フォントのファイルパス
    def __init__(self, screen, font):
        self.screen          = screen                           # スクリーン
        self.font            = font                             # 日本語フォントのファイルパス
        self.running         = True                             # メインループの管理
        self.current_screen  = FARSTSCREEN                      # 最初に描画する画面を設定
        self.previous_screen = self.current_screen              # 直前の画面
        self.veiw_popup      = ""                               # 表示するポップアップの管理
        self.flag_popup      = False                            # ポップアップ表示フラグ
        self.window_size     = pygame.display.get_window_size() # 画面の大きさを取得
        self.setting_screen()                                   # 表示する画面を設定
        self.setting_popup()
        self.setting_vital()                                    # 稼働状況表示の初期化 
        self.setting_fps()                                      # FPSを設定
        self.setting_background()                               # 背景を設定
        
    #   画面の登録
    def setting_screen(self):
        #   表示する画面を代入
        self.screens = {
            MAIN        : MainFrame(self.screen, self.font),
            DATA        : DataFrame(self.screen, self.font),
            PASS        : PassFrame(self.screen, self.font),
            IMAGE       : GraphFrame(self.screen, self.font),
            COUNT       : CountFrame(self.screen, self.font),
            MOTION_TEST : MotionTestFrame(self.screen, self.font),
            TEST01      : Test01Frame(self.screen, self.font),
            TEST02      : Test02Frame(self.screen, self.font),
            UPDATE_PASS : ChangePassScreen(self.screen, self.font)
        }

    def setting_popup(self):
        self.popups = {
            END              : EndPopup(self.screen, self.font),
            STOP_MOVE        : WorningPopup(self.screen, self.font),
            NOT_PASS         : PassErrorPopup(self.screen, self.font, NOT_PASS),
            DIFFER_PASS      : PassErrorPopup(self.screen, self.font, DIFFER_PASS),
            NONE_PASS        : BasePopup(self.screen, self.font, NONEPASSTEXT),
            CHANGE_PASS      : BasePopup(self.screen, self.font, CHANGEPASSTEXT),
            ERROR_POPUP      : ErrorPopup(self.screen, self.font),
            NO_DATA          : BasePopup(self.screen, self.font, NO_DATA_TEXT),
            DB_RESET         : DBresetPopup(self.screen, self.font),
            DB_RESET_SUCCESS : BasePopup(self.screen, self.font, DB_RESET_TEXT)
        }
    
    #   背景の設定
    def setting_background(self):
        if self.current_screen in BACKGROUNDIMAGE.keys():
            backgroud_image = pygame.image.load(BACKGROUNDIMAGE[self.current_screen])
            self.backgroud_image = pygame.transform.scale(backgroud_image, self.window_size)

    #   フレームレート設定      後でコメントをかく
    def setting_fps(self):
        self.clock = pygame.time.Clock()
        self.clock.tick(FPS)
        self.tcnt = 0
    
    #   稼働状況の初期設定
    def setting_vital(self):
        self.text_vital = FARSTVITAL
        self.font_vital = pygame.font.Font(self.font, 30)   #   稼働状況描画用フォントを設定
        self.vital, self.rect_vital, self.point_vital = Vital.setting_vital(self.text_vital,self.font_vital)
    
    #   暗転
    def brackout(self):
        print(self.current_screen)
        #   暗転処理
        screen = self.screens[self.previous_screen]      #   表示する画面を呼び出す
        BlackOut.brackout_screen(self.screen,self.backgroud_image, screen.draw)
        screen = self.screens[self.current_screen]
        screen.draw()
        self.setting_background()
        BlackOut.lightchenge_screen(self.screen,self.backgroud_image, screen.draw)
        self.previous_screen = self.current_screen

    # ポップアップの描画処理
    def draw_popup(self):
        button_lespons = None
        popup = self.popups[self.veiw_popup]

        while self.flag_popup:
            popup.draw()
            button_lespons = popup.update()
            pygame.display.update()
            if button_lespons:
                self.flag_popup = False
        
        if self.veiw_popup == END and button_lespons == "yes":
            self.running = False
            self.flag_popup = False
        elif self.veiw_popup == CHANGE_PASS:
            self.current_screen = MOTION_TEST
        if button_lespons == DB_RESET_SUCCESS:
            self.flag_popup = True
            popup = self.popups[button_lespons]
            while self.flag_popup:
                popup.draw()
                button_lespons = popup.update()
                pygame.display.update()
                if button_lespons:
                    self.flag_popup = False

    # ボタンの戻り値に応じた処理
    def judgement_action(self, action):
        if action == PASS:
            if self.text_vital == Vital.OPERATIONSTOPED:
                self.current_screen = action
            else:
                self.veiw_popup = STOP_MOVE
                self.flag_popup = True
        elif action in self.popups.keys():
                self.veiw_popup = action
                self.flag_popup = True
        elif action:
            self.current_screen = action
    
    #   動作処理
    def run(self):
        while self.running:                                 #   動作フラグが真(ON)の間
            self.clock.tick(15)
            if self.current_screen != self.previous_screen:
                self.brackout()
            screen = self.screens[self.current_screen]      #   表示する画面を呼び出す
            self.setting_background()
            self.screen.blit(self.backgroud_image, (0,0))
            screen.draw()                                   #   画面を描画
            self.text_vital, self.tcnt = Vital.update_vital(self.tcnt, self.text_vital)
            Vital.draw_vital(self.screen, self.text_vital,  self.point_vital, self.rect_vital,self.font_vital)
            action = screen.update()                        #   ボタンなどの処理を実行
            self.judgement_action(action)
            if self.flag_popup:
                self.draw_popup()
            pygame.display.update()
