#パスワード変更画面
from screen.PassFrame import PassFrame
from parts.SQLCommunication_main import SQLCommunication
from parts.Picture import Picture
from popup.BasePopup import BasePopup
from popup.PassErrorPopup import PassErrorPopup
from parts.Button import Button
from filepath import *
import pygame

# パスワード保存先　pass_mun

# 使用クエリ
GETPASSWORD = "SELECT num FROM pass_num"
CHANGEPASSWORD = "UPDATE pass_num SET num = "
# 使用画像のファイルパス
RETRYPASSWORDTEXT = IMAGEFILEPATH + "exptxt\\pic72.png"
NEWPASSWORDTEXT = IMAGEFILEPATH + "exptxt\\pic73.png"

RETRYPOPUPMSG = "再入力されたパスワードが違います"
NOTPASSWORDMSG = "新しいパスワードを入力してください"
UPDATEMSG = "パスワードを変更しました" 

class ChangePassScreen(PassFrame):
    def __init__(self, screen, font=None):
        super().__init__(screen, font)
        self.db = SQLCommunication()
        self.flag_retry = False
        self.flag_popup = ""
        self.new_password = ""
        self.old_pass = self.acpuisition_pass()
        self.buttons[0] = Button(self.screen, 0, 960, 330, 120, IMAGEFILEPATH + "button\\back.png",  self.move_motiontest)
        self.images = {
            Picture(self.screen, 0, 0, 600, 200, IMAGEFILEPATH + "title\\pic78.png"),
            Picture(self.screen, 410, 200, 180, 180, IMAGEFILEPATH + "button\\pic19.png")
        }
        self.gaid_images = {
            "new_password" : Picture(self.screen, 590, 40, 850, 200, NEWPASSWORDTEXT),
            "retry_password" : Picture(self.screen, 635, 40, 750, 200, RETRYPASSWORDTEXT)
        }
        self.popups = {
            "retry"   : PassErrorPopup(self.screen, font, "reset"),
            "notpass" : BasePopup(self.screen, font, NOTPASSWORDMSG),
            "update"  : BasePopup(self.screen, font, UPDATEMSG)
        }

    #   ボタン及びテキストの描画処理を記述
    def draw(self):
        for image in self.images:
            image.draw()
        if self.flag_retry:
            self.gaid_images["retry_password"].draw()
        else:
            self.gaid_images["new_password"].draw()
        self.draw_pass()
        for button in self.buttons:
            button.draw()
        if self.flg_veiw_popup:
            while self.flag_popup:
                self.popups[self.flag_popup].draw()
                if self.popups[self.flag_popup].update():
                    self.flag_popup = False
                pygame.display.update()

    def acpuisition_pass(self):
        acequired_data = self.db.db_query_execution("testdb_main.db", GETPASSWORD)
        print(GETPASSWORD)
        old_pass = acequired_data[0][0]
        if type(old_pass) == str:
            return old_pass
        return None
        
    def update_popup(self):
        popup = self.popups["update"]
        view_flg = True
        while view_flg:
            popup.draw()
            if popup.update():
                view_flg = False
            pygame.display.update()
            
    
    def num_check(self):
        if self.flag_retry:
            if self.set_pass == self.new_password:
                query = CHANGEPASSWORD + self.new_password
                self.db.db_query_execution("testdb_main.db", query)
                self.update_popup()
                self.flag_retry = False
                self.set_pass = ""
                return "motiontest"
            else:
                self.flag_popup = "retry"
                self.set_pass = ""
                self.flg_veiw_popup = True
                self.flag_retry = False
        elif self.set_pass:
            self.new_password = self.set_pass
            self.set_pass = ""
            self.flag_retry = True
        else:
            self.set_pass = ""
            self.flag_popup = "notpass"
            self.flg_veiw_popup = True
    
    def move_motiontest(self):
        self.flag_retry = False
        self.set_pass = ""
        return "motiontest"