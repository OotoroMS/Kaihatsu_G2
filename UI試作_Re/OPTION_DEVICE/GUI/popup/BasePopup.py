import pygame
from typing import Tuple, Optional
# 定数
from GUI.constant.file_path         import *
from GUI.constant.color             import *
from GUI.constant.popup.popup_name  import *
# 部品
from GUI.parts.Button           import *
from GUI.parts.Picture          import *
from GUI.parts.CaluclatePopup   import *

FONT_SIZE   = 100
CALC_CENTER = 2

class BasePopup:
    def __init__(self, screen : pygame.Surface) -> None:
        self.screen = screen
        self.text_font = pygame.font.Font(FONT, FONT_SIZE)
        # ポップアップのサイズを計算
        self.rect = self.create_popup_rect()
        # 画面の中心を取得
        self.center_whidh = self.width // CALC_CENTER
        # ボタンと画像を生成
        self.setting_images()
        self.setting_buttons()
        
    # popupの画面を生成
    def create_popup_rect(self) -> Optional[pygame.rect.Rect]:
        # 画面のサイズを取得
        self.base_width, self.base_height = pygame.display.get_window_size()
        # 取得した画面サイズからポップアップのサイズと座標を取得
        self.width, self.height = calculate_popup_size(self.base_width, self.base_height)
        self.pos_x, self.pos_y  = caluclate_popup_position(self.base_width,self.base_height, self.width, self.height)
        # 生成可能ならば表示用の矩形を生成
        if self.pos_x and self.pos_y:
            return pygame.rect.Rect(self.pos_x, self.pos_y, self.width, self.height)
        else:
            return None
        
    # 画像設定
    def setting_images(self):
        self.images = []

    # ボタン設定
    def setting_buttons(self):
        self.buttons = []
    
    # 更新処理
    def click_event(self):
        result = None
        nomarl = False
        for event in pygame.event.get():
            result, nomarl = self.event_button_down(event)
            if nomarl:
                return result, nomarl
        return result, nomarl
    
    # 押下時のイベント処理
    def event_button_down(self, event):
        result = None
        nomarl = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            result, nomarl = self.clicked(event)
            if nomarl:
                return result, nomarl
        return result, nomarl
    
    # クリック判定
    def clicked(self, event):
        result = None
        nomarl = False
        for button in self.buttons:
            if type(button) == Button:
                result, nomarl = button.is_clicked(event)
                if nomarl:
                    return result, nomarl
        return result, nomarl

    # 描画
    def draw(self):
        if self.rect:
            pygame.draw.rect(self.screen, GRAY, self.rect)
            pygame.draw.rect(self.screen, BLACK, self.rect, 2)
            for image in self.images:
                if type(image) == Picture:
                    image.draw()
            for button in self.buttons:
                if type(button) == Button:
                    button.draw()
        else:
            print("popup drow(): 矩形の生成に失敗しています")
