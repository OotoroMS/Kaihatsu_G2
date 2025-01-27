import pygame
from typing import Tuple, Optional
from MAIN_OPRATION.GUI.Popups.BasePopup            import BasePopup
from MAIN_OPRATION.GUI.Constants.popup_text  import *
from MAIN_OPRATION.GUI.Constants.popup_name  import *
from MAIN_OPRATION.GUI.Constants.file_path         import *
from MAIN_OPRATION.GUI.Constants.judge_result      import *
from MAIN_OPRATION.GUI.Constants.color             import *

from MAIN_OPRATION.GUI.Parts.Button   import Button
from MAIN_OPRATION.GUI.Parts.Picture  import Picture

IMAGE_SIZE     = (250, 150)
IMAGEDISTANSE  = 50
TEXTDISTANSE   = 200
BUTTON_BACK    = BUTTON_FILE_PATH + "\\button_back.png"
WORNING_IMAGE  = EXPTXT_FILE_PATH + "\\exptxt_warning.png"

class StopPopup(BasePopup):
    def __init__(self, screen: pygame.Surface) -> None:
        super().__init__(screen)
        self.text_list = POPUP_TEXT[STOP_POPUP]
        self.text_top  = self.text_font.render(self.text_list[0], True, WHITE)
        self.text_mid  = self.text_font.render(self.text_list[1], True, WHITE)
        self.text_bot  = self.text_font.render(self.text_list[2], True, WHITE)
        image_x        = self.pos_x + (self.width // 2) - (IMAGE_SIZE[0] // 2)
        image_y        = self.pos_y + 25
        button_x       = self.pos_x + self.width // 2 - self.width // 8
        button_y       = self.height - self.height // 4
        button_width   = self.width // 4
        buttn_height   = self.height // 4
        self.image     = Picture(self.screen, (image_x,  image_y),  IMAGE_SIZE, WORNING_IMAGE)
        self.button    = Button(self.screen,  (button_x, button_y), (button_width, buttn_height), BUTTON_BACK,self.close_popup)
    # 描画処理
    def draw(self):
        pygame.draw.rect(self.screen, GRAY, self.rect)
        pygame.draw.rect(self.screen, BLACK, self.rect, 2)
        self.text_draw()
        self.image.draw()
        self.button.draw()
    
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
        result, nomarl = self.button.is_clicked(event)
        return result, nomarl

    def text_draw(self):
        text_top_width  = self.text_top.get_width()     
        text_top_height = self.text_top.get_height()
        text_top_y      = self.pos_y + TEXTDISTANSE              # text_topのy座標
        
        text_middle_width  = self.text_mid.get_width()
        text_middle_height = self.text_mid.get_height()
        text_middle_y      = text_top_y + text_top_height        # text_middleのy座標

        text_bottom_width = self.text_bot.get_width()
        text_bottom_y     = text_middle_y + text_middle_height   # text_bottomの座標

        # (self.pos_x + (self.width - text_width) // 2)でテキストをポップアップの中央に設定している
        self.screen.blit(self.text_top, ((self.pos_x + (self.width - text_top_width)     // 2),  text_top_y))
        self.screen.blit(self.text_mid, ((self.pos_x + (self.width - text_middle_width)  // 2),  text_middle_y))
        self.screen.blit(self.text_bot, ((self.pos_x + (self.width -  text_bottom_width) // 2),  text_bottom_y))

    def close_popup(self):
        return None, True