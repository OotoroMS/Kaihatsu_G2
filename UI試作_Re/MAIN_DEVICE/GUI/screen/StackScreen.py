# 動作確認画面(移動部)
import pygame
# 基本画面
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
# シリアル通信クラス
from SERIAL.manager.SerialUIBridge  import SerialUIBridge
# タイトルの設定
STACK_TITLE_STATUS = {
    "coordinate" : (0,   0),
    "size"       : (750, 200),
    "image_path" : TITLE_FILE_PATH + "title_stack.png"#蓄積部
}
# ボタンの設定
CYLINDER_DOWN_BUTTON_STATUS        = {
    "coordinate" : (1000, 510),
    "size"       : (600, 280),
    "image_path" : BUTTON_FILE_PATH + "button_cylinder_down.png"#上下シリンダ下降
}

BACK_BOTTON_STATUS                = {
    "coordinate" : (0, 960),
    "size"       : (330, 120),
    "image_path" : BUTTON_FILE_PATH + "button_back.png"
}
# 画像の設定
STACK_SENSOR_EXPTXT_STATUS = {
    "coordinate" : (1000,220),
    "size"       : (600, 240),
    "image_path" :EXPTXT_FILE_PATH + "exptxt_stack_sensor.png"#蓄積部センサ
}
CYLINDER_UP_EXPTXT_STATUS = {
    "coordinate" : (250,520),
    "size"       : (600, 240),
    "image_path" :EXPTXT_FILE_PATH + "exptxt_cylinder_up.png"#上下シリンダ上昇
}
# ランプの設定
STACK_SENSOR_LAMP_STATUS = {
    "x"      : 1490,
    "y"      : 300,
    "w"      : 60,
    "h"      : 60,
    "color"  : GRAY
}
CYLINDER_UP_LAMP_STATUS = {
    "x"      : 745,
    "y"      : 620,
    "w"      : 60,
    "h"      : 60,
    "color"  : GRAY
}
TERMINATION = "動作完了"
STACK_SENSOR = "stack_sensor"
CYLINDER_UP = "cylinder_up"
CYLINDER_DOWN = "cylinder_down"
COMAND = {
    CYLINDER_DOWN : ("シリンダ下降", "蓄積部")
}

class StackScreen(BaseScreen):
    def __init__(self, screen: pygame.Surface, serial : SerialUIBridge):
        super().__init__(screen)
        self.serial = serial
        self.setting_lamps()
    
    # 各ボタンの設定
    def setting_buttons(self):
        self.buttons = [
            Button(self.screen, **BACK_BOTTON_STATUS, func=self.move_motion)
        ]
        self.lamp_buttons = [
            LampButton(self.screen, **CYLINDER_DOWN_BUTTON_STATUS,       func=self.cylinder_down)
        ]
    
    # 各画像の設定
    def setting_images(self):
        self.images = [
            Picture(self.screen, **STACK_TITLE_STATUS),
            Picture(self.screen, **STACK_SENSOR_EXPTXT_STATUS),
            Picture(self.screen, **CYLINDER_UP_EXPTXT_STATUS)
        ]
    
    def setting_lamps(self):
        self.lamps = {
            STACK_SENSOR : Lamp(self.screen, **STACK_SENSOR_LAMP_STATUS),
            CYLINDER_UP : Lamp(self.screen, **CYLINDER_UP_LAMP_STATUS)
        }

    def draw(self):
        for image  in self.images:
            image.draw()
        for button in self.buttons:
            button.draw()
        for button in self.lamp_buttons:
            button.draw()
        message = self.serial.process_serial_queue()
        for key   in self.lamps:
            if message[0][0] == "蓄積部センサ" and key == STACK_SENSOR:
                self.lamps[key].update_color(GREEN)
            else:
                self.lamps[key].update_color(YELLOW)
            if message[0][0] == "上下シリンダ上昇" and key == CYLINDER_UP:
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
        self.serial.send_Set(COMAND[result])
        button.update_lamp_color(GREEN)
        while True:
            button.draw()
            pygame.display.update()
            messege = self.serial.process_serial_queue()
            if messege and messege[0][0] == TERMINATION:
                break
        button.update_lamp_color(YELLOW)
        button.draw()
        pygame.display.update()
    
    # 動作選択画面に戻る
    def move_motion(self):
        return MOTION, OK
    
    # シリンダを下降させる
    def cylinder_down(self):
        return CYLINDER_DOWN, True
