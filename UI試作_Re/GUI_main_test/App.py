#   画面サイズ  1024x600
import pygame
import Vital
#   自作のクラス
from MainFrame import MainFrame
from DataFrame import DataFrame
from PassFrame import PassFrame
from GraphFrame import GraphFrame
from CountFrame import CountFrame
from BasePopup import BasePopup
from TestFrame import TestFrame

import BrackOut

#   カラーコード
BLACK = ((0,0,0))
GRAY  = ((200,200,200))
#   動作一覧画面
OPERATION = "pass"
#   背景画像
BACKGROUND_IMAGE = {
    "main" : "D:\\Kaihatsu\\VScode\\GUI\\GUI_main_test\\image\\watercolor_00685.jpg",
    "pass" : "D:\\Kaihatsu\\VScode\\GUI\\GUI_main_test\\image\\pass.jpg"
}
POPUPMSG = "装置を停止してください"


class App:
    #   screen : pygameのスクリーン,font : 日本語フォントのファイルパス
    def __init__(self, screen, font):
        self.screen = screen                                #   スクリーン
        self.font = font                                    #   日本語フォントのファイルパス
        self.running = True                                 #   メインループの管理
        self.current_screen = "main"                        #   最初に描画する画面を設定
        self.previous_screen = self.current_screen          #   直前の画面
        self.veiw_popup = False                             #   ポップアップ表示フラグ
        self.setting_screen()                               #   表示する画面を設定
        self.setting_vital()                                #   稼働状況表示の初期化 
        self.setting_fps()                                  #   FPSを設定
        self.setting_background()
        
    #   画面の登録
    def setting_screen(self):
        #   表示する画面を代入
        self.screens = {
            "main"  :   MainFrame(self.screen, self.font),
            "data"  :   DataFrame(self.screen, self.font),
            "pass"  :   PassFrame(self.screen, self.font),
            "graph" :   GraphFrame(self.screen, self.font),
            "count" :   CountFrame(self.screen, self.font),
            "test"  :   TestFrame(self.screen, self.font),
            "move_popup"   :   BasePopup(self.screen,self.font, POPUPMSG)
        }

    #   背景の設定
    def setting_background(self):
        if self.current_screen == "main" or self.current_screen == "pass":
            backgroud_image = pygame.image.load(BACKGROUND_IMAGE[self.current_screen])
            self.backgroud_image = pygame.transform.scale(backgroud_image, (1980, 1080))

    #   フレームレート設定      後でコメントをかく
    def setting_fps(self):
        self.clock = pygame.time.Clock()
        self.clock.tick(120)
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
        BrackOut.brackout_screen(self.screen,self.backgroud_image, screen.draw)
        screen = self.screens[self.current_screen]
        screen.draw()
        self.setting_background()
        BrackOut.lightchenge_screen(self.screen,self.backgroud_image, screen.draw)
        self.previous_screen = self.current_screen

    #   
    def update_cureent_screen(self, action):
        if action == "pass":
            if self.text_vital == Vital.OPERATIONSTOPED:
                self.current_screen = action
            else:
                self.veiw_popup = True
        elif action == "end":   
                self.running = False
        elif action:
            self.current_screen = action
    
    #   動作処理
    def run(self):
        while self.running:                                 #   動作フラグが真(ON)の間
            if self.current_screen != self.previous_screen:
                self.brackout()
            screen = self.screens[self.current_screen]      #   表示する画面を呼び出す
            self.setting_background()
            self.screen.blit(self.backgroud_image, (0,0))
            screen.draw()                                   #   画面を描画
            if self.veiw_popup:
                self.screens["move_popup"].draw()
                self.veiw_popup = self.screens["move_popup"].update()
            self.text_vital, self.tcnt = Vital.update_vital(self.tcnt, self.text_vital)
            Vital.draw_vital(self.screen, self.text_vital,  self.point_vital, self.rect_vital,self.font_vital)
            action = screen.update()                        #   ボタンなどの処理を実行
            self.update_cureent_screen(action)
            pygame.display.update()
