# 動作確認画面(移動部)
import pygame
# 基本画面
from SERIAL.manager.SerialUIBridge  import SerialUIBridge
from GUI.screen.BaseScreen import BaseScreen
# 部品
from GUI.parts.Button       import Button
from GUI.parts.Picture      import Picture
from GUI.parts.ButtonAtLamp import ButtonAtLamp as LampButton
from GUI.parts.Lamp         import Lamp
# 定数
from constant.file_path   import *
from constant.screen_name import *
from constant.color       import *
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
    def __init__(self, screen: pygame.Surface, serial : SerialUIBridge):
        super().__init__(screen)
        self.serial = serial
        self.prese = False
        self.setting_lamps()
    
    # 各ボタンの設定
    def setting_buttons(self):
        self.buttons = [
            Button(self.screen,**BACK_BOTTON_STATUS, func=self.move_motion)
        ]
        self.motion_buttons = [
            Button(self.screen,     **ABSORPTION_BUTTON_STATUS,    func=self.adsorption_on), # 吸着ON
            LampButton(self.screen, **CYLINDER_UP_BUTTON_STATUS,   func=self.cylinder_up),
            LampButton(self.screen, **CYLINDER_DOWN_BUTTON_STATUS, func=self.cylinder_down)
            
        ]
        self.presed_buttons = [
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
        for button in self.motion_buttons:
            button.draw()
        for button in self.presed_buttons:
            button.draw()
        message = self.serial.process_serial_queue()
        for key   in self.lamps:
            if message[0][0] == "移動中のワークを検知" and key == MOVE_WORK:
                self.lamps[key].update_color(GREEN)
            else:
                self.lamps[key].update_color(YELLOW)
            self.lamps[key].draw()

    # 押下判定
    def click_event(self):
        result = None
        normal = None
        for event in pygame.event.get():
                result, normal = self.clicked(event)
                return result, normal
        if self.prese:
            print("prese command :", self.command)
            self.serial.send_set("辞書型コマンド[self.command]")
            return True, OK

        return result, NG

    def clicked(self, event):
        result = ""
        normal = False
        # ボタンに位置でクリック(タップ)されていたら紐づけられた処理を行う
        for button in self.buttons:
            result,normal = button.is_clicked(event)
            if normal:
                return result, normal
        for button in self.motion_buttons:
            result,normal = button.is_clicked(event)
            if result:
                self.lamp_button_clicked(button, result)
                return result, normal
        for button in self.presed_buttons:
            result,normal = button.is_pressed(event)
            if normal:
                print(normal)
                self.button_presed(button, result)
                return result, normal
            else:
                if type(button) == LampButton:
                    button.update_lamp_color(GRAY)     
        return result, normal

    def lamp_button_clicked(self, button, result):
        self.serial.send_set("辞書型コマンド[result]")
        if type(button) == LampButton:
            button.update_lamp_color(YELLOW)
        while True:
            button.draw()
            pygame.display.update()
            messege = self.serial.process_serial_queue()
            if messege and messege[0][0] == TERMINATION:
                break
        button.update_lamp_color(GREEN)
        button.draw()
        pygame.display.update()
    
    def button_presed(self, button, result):
        if result:
            self.prese = True
            self.command = result
        else:
            self.prese   = False
            self.command = None
        if type(button) == LampButton:
            button.update_lamp_color(GREEN)
            button.draw()
            pygame.display.update()

    # 動作確認画面(メインメニュー)に戻る
    def move_motion(self):
        return MOTION, OK
    def adsorption_on(self):
        return "処理に対応するkeyを返す", True
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
