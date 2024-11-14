#   画面サイズ  1024x600
import pygame
import parts.Vital as Vital
#   自作のクラス
from screen.MainFrame        import MainFrame
from screen.DataFrame        import DataFrame
from screen.PassFrame        import PassFrame
from screen.GraphFrame       import GraphFrame
from screen.CountFrame       import CountFrame
from screen.MotionTestFrame  import MotionTestFrame
from screen.Test01Frame      import Test01Frame
from screen.Test02Frame      import Test02Frame
from screen.Test03Frame      import Test03Frame
from screen.Test04Frame      import Test04Frame
from screen.ChangePassScreen import ChangePassScreen
from popup.BasePopup         import BasePopup
from popup.EndPopup          import EndPopup
from popup.WarningPopup      import WorningPopup
from popup.ErrorPopup        import ErrorPopup
from popup.PassErrorPopup    import PassErrorPopup
from filepath                import *
from comunication.pc_comands import *
import Blackout

#   カラーコード
BLACK = ((0,0,0))
GRAY  = ((200,200,200))

#   動作一覧画面
OPERATION = "pass"
#   背景画像
BACKGROUND_IMAGE = {
    "main" : IMAGEFILEPATH + "background\\back01.jpg",
    "pass" : IMAGEFILEPATH + "background\\back02.jpg",
    "motiontest" : IMAGEFILEPATH + "background\\back01.jpg"
}
POPUPMSG = "装置を停止してください"
ENDPOPUP = "終了しますか？"
END      = "end"

class App:
    #   screen : pygameのスクリーン,font : 日本語フォントのファイルパス
    def __init__(self, screen, font, serial : PCManager):
        self.screen = screen                                #   スクリーン
        self.font = font                                    #   日本語フォントのファイルパス
        self.running = True                                 #   メインループの管理
        self.current_screen = "main"                        #   最初に描画する画面を設定
        self.previous_screen = self.current_screen          #   直前の画面
        self.popup_flg = False                              #   ポップアップ表示フラグ
        self.veiw_popup = ""
        self.serial = serial
        self.setting_screen()                               #   表示する画面を設定
        self.setting_popup()
        self.setting_vital()                                #   稼働状況表示の初期化 
        self.setting_fps()                                  #   FPSを設定
        self.setting_background()
        
    #   画面の登録
    def setting_screen(self):
        #   表示する画面を代入
        self.screens = {
            "main"       :   MainFrame(self.screen, self.font),
            "data"       :   DataFrame(self.screen, self.font),
            "pass"       :   PassFrame(self.screen, self.font),
            "graph"      :   GraphFrame(self.screen, self.font),
            "count"      :   CountFrame(self.screen, self.font),
            "motiontest" :   MotionTestFrame(self.screen, self.font),
            "test01"     :   Test01Frame(self.screen, self.font),
            "test02"     :   Test02Frame(self.screen, self.font),
            "test03"     :   Test03Frame(self.screen, self.font),
            "test04"     :   Test04Frame(self.screen, self.font),
            "changepass" :   ChangePassScreen(self.screen, self.font)
        }

    def setting_popup(self):
        self.popups = {
            "end"        : EndPopup(self.screen,  self.font, ENDPOPUP),
            "pass_stop"  : WorningPopup(self.screen, self.font),
            "error"      : ErrorPopup(self.screen, self.font),
            "not_pass"   : PassErrorPopup(self.screen, self.font, "retry"),
            "db_reset"   : BasePopup(self.screen, self.font, "データを削除しました"),
            "none_data"  : BasePopup(self.screen, self.font, "データが存在しません")
        }

    #   背景の設定
    def setting_background(self):
        if self.current_screen == "main" or self.current_screen == "pass":
            backgroud_image = pygame.image.load(BACKGROUND_IMAGE[self.current_screen])
            self.backgroud_image = pygame.transform.scale(backgroud_image, (1980, 1080))
        elif self.current_screen == "motiontest":
            backgroud_image = pygame.image.load(BACKGROUND_IMAGE[self.current_screen])
            self.backgroud_image = pygame.transform.scale(backgroud_image, (1980, 1080))

    #   フレームレート設定      後でコメントをかく
    def setting_fps(self):
        self.clock = pygame.time.Clock()
        self.clock.tick(60)
        self.tcnt = 0
        self.fps = 60
    
    #   稼働状況の初期設定
    def setting_vital(self):
        self.text_vital = "稼働中"
        self.font_vital = pygame.font.Font(self.font, 30)   #   稼働状況描画用フォントを設定
        self.vital, self.rect_vital, self.point_vital = Vital.setting_vital(self.text_vital,self.font_vital)
    
    #   暗転
    def brackout(self):
        print(self.current_screen)
        #   暗転処理
        screen = self.screens[self.previous_screen]      #   表示する画面を呼び出す
        Blackout.brackout_screen(self.screen,self.backgroud_image, screen.draw)
        screen = self.screens[self.current_screen]
        screen.draw()
        self.setting_background()
        Blackout.lightchenge_screen(self.screen,self.backgroud_image, screen.draw)
        self.previous_screen = self.current_screen

    #   
    def update_cureent_screen(self, action):
        if action == "pass":
            if self.text_vital == Vital.OPERATIONSTOPED:
                self.current_screen = action
            else:
                self.popup_flg = True
                self.veiw_popup = "pass_stop"
        elif action in self.popups.keys():
            self.popup_flg = True
            self.veiw_popup = action
        elif action in self.screens.keys():
            self.current_screen = action
    
    def draw_popup(self, action):
        button_lespons = None
        while self.popup_flg:
            self.popups[self.veiw_popup].draw()
            button_lespons = self.popups[self.veiw_popup].update()
            if button_lespons != None:
                self.popup_flg = False
            pygame.display.update()
        if action == END and button_lespons == "yes":
            self.running = False
        if self.veiw_popup == "error":
            self.text_vital = "稼働中"
        
    #   動作処理
    def run(self):
        while self.running:                                 #   動作フラグが真(ON)の間
            self.clock.tick(60)
            if self.current_screen != self.previous_screen:
                self.brackout()
            screen = self.screens[self.current_screen]      #   表示する画面を呼び出す
            self.setting_background()
            self.screen.blit(self.backgroud_image, (0,0))
            screen.draw()                                   #   画面を描画
            sirial_result = self.serial.read()
            if sirial_result:
                vaital = sirial_result[0]
                plase  = sirial_result[1]
                if vaital[:3] == "エラー":
                    self.text_vital = vaital[:3]
            if self.text_vital != "エラー":                
                self.text_vital, self.tcnt = Vital.update_vital(self.tcnt, self.text_vital)
            Vital.draw_vital(self.screen, self.text_vital,  self.point_vital, self.rect_vital,self.font_vital)
            if self.text_vital == "エラー" :
                self.popup_flg = True
                self.veiw_popup = "error"
                self.popups[self.veiw_popup].update_error_masage(vaital, plase)
            action = screen.update()                        #   ボタンなどの処理を実行
            self.update_cureent_screen(action)
            if self.popup_flg:
                self.draw_popup(action)
            pygame.display.update()
