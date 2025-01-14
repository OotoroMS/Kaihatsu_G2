import pygame
from typing               import Tuple, Optional
from parts.CaluclatePopup import *
from popup.BasePopup      import BasePopup
from parts.Button         import Button
from constant.FilePath    import *
from constant.PopupName   import *
from DB.SQLCommunication import SQLCommunication

GRAY = ((200,200,200))      #   カラーコード(灰色)
BLACK = ((255,255,255))     #   カラーコード(黒)
WHITE = ((0,0,0))           #   カラーコード(白)
BASEMSSEGE = "BASE POPUP"
BACKFRAME = BUTTONFILEPATH + "back.png"#戻る
ENDFRAME  = BUTTONFILEPATH + "pic04.png"#04終了
BASEPASH = EXPTXTFILEPATH  + "pic75.png"#FAILアイコン

DB_RESET_TEXT = "データベースをリセットしますか？"
DBNAME        = "testdb_main.db" 
QUERY         = "DELETE FROM %s"
TARGETTABLE = [
    "db_now",
    "db_countlog",
    "db_timelog",
    "db_sizelog"
]

class DBresetPopup(BasePopup):
    def __init__(self, screen : pygame.Surface, font : pygame.font.Font):
        print("DBreset")
        super().__init__(screen, font, "")
        self.text_font = pygame.font.Font(font, 100)
        self.rect = self.create_popup_rect()
        self.text = DB_RESET_TEXT
        self.view_text = self.text_font.render(self.text, True, WHITE)
        self.buttons = {
            Button(self.screen, (self.width // 2) - (self.width // 4), self.height - (self.height // 4) , self.width // 4,self.height//4, ENDFRAME,  self.YES),     
            Button(self.screen, (self.width // 2) + (self.width // 8), self.height - (self.height // 4) , self.width // 4,self.height//4, BACKFRAME, self.NO)
        }
        self.db = SQLCommunication()
        self.db.set_db_name(DBNAME)

    def create_popup_rect(self) -> Optional[pygame.rect.Rect]:
        """
        popup画面の範囲を計算し、表示領域を生成するモジュール。
        """
        self.base_width, self.base_height = pygame.display.get_window_size()
        self.width, self.height = calculate_popup_size(self.base_width, self.base_height)
        self.pos_x, self.pos_y = caluclate_popup_position(self.base_width,self.base_height, self.width, self.height)
        if self.pos_x and self.pos_y:
            return pygame.rect.Rect(self.pos_x, self.pos_y, self.width, self.height)
        else:
            return None
    
    def update(self):
        move = None
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in self.buttons:
                    move = button.is_clicked(event)
                    if move:
                        break
        return move

    def draw(self):
        """
        画面更新処理。
        """
        if self.rect:
            pygame.draw.rect(self.screen, GRAY, self.rect)
            pygame.draw.rect(self.screen, BLACK, self.rect, 2)
            view_text_width = self.view_text.get_width()
            view_text_x = self.pos_x + ((self.width - view_text_width) // 2)
            print("veiw_text_whidth :",view_text_width, "self.width :", view_text_x)
            self.screen.blit(self.view_text, (view_text_x, self.height // 2))
            for button in self.buttons:
                button.draw()
        else:
            print("失敗")              
    
    def YES(self):#実際は削除するがテストでは消さない
        # for table in TARGETTABLE:
        #     delete_query = QUERY % table
        #     print("変更前")
        #     self.db.table_data_list_display(table_name=table)
        #     self.db.db_query_execution(query=delete_query)
        #     print("変更後")
        #     self.db.table_data_list_display(table_name=table)
        print("db_reset")
        return DB_RESET_SUCCESS
    
    def NO(self):
        print("db_reset_cancel")
        return True