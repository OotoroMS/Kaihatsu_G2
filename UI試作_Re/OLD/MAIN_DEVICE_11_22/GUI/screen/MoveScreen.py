# 動作確認画面(移動部)
import pygame
# 基本画面
from SERIAL.pc_comands     import *
from GUI.screen.BaseScreen import BaseScreen
# 部品
from GUI.parts.Button       import Button
from GUI.parts.Picture      import Picture
from GUI.parts.ButtonAtLamp import ButtonAtLamp as LampButton
from GUI.parts.Lamp         import Lamp
# 定数
from GUI.constant.file_path   import *
from GUI.constant.screen_name import *
from GUI.constant.color       import *
# タイトルの設定
MOVE_TITLE_STATUS = {
    "coordinate" : (0,   0),
    "size"       : (750, 200),
    "image_path" : TITLE_FILE_PATH + "title_move.png"
}
# ボタンの設定
ABSORPTION_BUTTON_STATUS        = {
    "coordinate" : (350, 190),
    "size"       : (550, 250),
    "image_path" : BUTTON_FILE_PATH + "button_adsorption.png"
}
CYLINDER_UP_BUTTON_STATUS       = {
    "coordinate" : (350, 490),
    "size"       : (550, 250),
    "image_path" : BUTTON_FILE_PATH + "button_cylinder_up.png"
}
CYLINDER_DOWN_BUTTON_STATUS     = {
    "coordinate" : (1100,490),
    "size"       : (550, 250),
    "image_path" : BUTTON_FILE_PATH + "button_cylinder_down.png"
}
MOVE_MOTOR_NORMAL_BUTON_STATUS  = {
    "coordinate" : (350, 790),
    "size"       : (550, 250),
    "image_path" : BUTTON_FILE_PATH + "button_motor_normal.png"
}
MOVE_MOTOR_REVERSE_BUTON_STATUS = {
    "coordinate" : (1100,790),
    "size"       : (550, 250),
    "image_path" : BUTTON_FILE_PATH + "button_motor_reverse.png"
}
BACK_BOTTON_STATUS              = {
    "coordinate" : (0, 960),
    "size"       : (330, 120),
    "image_path" : BUTTON_FILE_PATH + "button_back.png"
}
# 画像の設定
MOVE_WORK_EXPTXT_STATUS = {
    "coordinate" : (1100,200),
    "size"       : (550, 240),
    "image_path" :EXPTXT_FILE_PATH + "exptxt_move_work.png"
}
# ランプの設定
MOVE_WORK_LAMP_STATUS = {
    "x"      : 1550,
    "y"      : 295,
    "w"      : 50,
    "h"      : 50,
    "color"  : GRAY
}
TERMINATION = "動作完了"
MOVE_WORK = "move_work"

class MoveScreen(BaseScreen):
    def __init__(self, screen: pygame.Surface, serial : PCManager):
        super().__init__(screen)
        self.serial = serial
        self.setting_lamps()
    
    # 各ボタンの設定
    def setting_buttons(self):
        self.buttons = [
            Button(self.screen,**BACK_BOTTON_STATUS, func=self.move_motion)
        ]
        self.lamp_buttons = [
            LampButton(self.screen, **CYLINDER_UP_BUTTON_STATUS,       func=self.cylinder_up),
            LampButton(self.screen, **CYLINDER_DOWN_BUTTON_STATUS,     func=self.cylinder_down),
            LampButton(self.screen, **MOVE_MOTOR_NORMAL_BUTON_STATUS,  func=self.motor_normal),
            LampButton(self.screen, **MOVE_MOTOR_REVERSE_BUTON_STATUS, func=self.motor_reverse) 
        ]
    
    # 各画像の設定
    def setting_images(self):
        self.images = [
            Picture(self.screen, **MOVE_TITLE_STATUS),
            Picture(self.screen, **MOVE_WORK_EXPTXT_STATUS)
        ]
    
    def setting_lamps(self):
        self.lamps = {
            MOVE_WORK : Lamp(self.screen, **MOVE_WORK_LAMP_STATUS)
        }

    def draw(self):
        for image  in self.images:
            image.draw()
        for button in self.buttons:
            button.draw()
        for button in self.lamp_buttons:
            button.draw()
        message = self.serial.read()
        for key   in self.lamps:
            if message == "移動中のワークを検知" and key == MOVE_WORK:
                self.lamps[key].update_color(GREEN)
            else:
                self.lamps[key].update_color(YELLOW)
            self.lamps[key].draw()

    def clicked(self, event):
        result = ""
        normal = False
        # ボタンに位置でクリック(タップ)されていたら紐づけられた処理を行う
        for button in self.buttons:
            result,normal = button.is_clicked(event)
            if normal:
                return result, normal
        for button in self.lamp_buttons:
            result,normal = button.is_clicked(event)
            if normal:
                self.lamp_button_clicked(button, result)
                return result, normal
        return result, normal
    
    def lamp_button_clicked(self, button: LampButton, result):
        self.serial.write_serial("辞書型コマンド[result]")
        button.update_lamp_color(GREEN)
        while True:
            button.draw()
            pygame.display.update()
            messege = self.serial.read()
            if messege and messege == TERMINATION:
                break
        button.update_lamp_color(YELLOW)
        button.draw()
        pygame.display.update()
    
    # 動作選択画面に戻る
    def move_motion(self):
        return MOTION, OK
    # シリンダーを上昇させる
    def cylinder_up(self):
        return "処理に対応するkeyを返す", True
    # シリンダを下降させる
    def cylinder_down(self):
        return "処理に対応するkeyを返す", True
    # モータを正転
    def motor_normal(self):
        return "処理に対応するkeyを返す", True
    # モータを逆転
    def motor_reverse(self):
        return "処理に対応するkeyを返す", True
