# 動作確認画面(投入・洗浄部)
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
WASH_TITLE_STATUS = {
    "coordinate" : (0,   0),
    "size"       : (750, 200),
    "image_path" : TITLE_FILE_PATH + "title_wash.png"
}

# ボタンの設定
BACK_BOTTON_STATUS                = {
    "coordinate" : (0, 960),
    "size"       : (330, 120),
    "image_path" : BUTTON_FILE_PATH + "button_back.png"
}
ECCENTRICITY_BUTTON_STATUS        = {
    "coordinate" : (1100,190),
    "size"       : (550, 250),
    "image_path" : BUTTON_FILE_PATH + "button_eccentricity.png"
}
CYRINDER_ADVANCE_BUTTON_STATUS    = {
    "coordinate" : (350, 490),
    "size"       : (550, 250),
    "image_path" : BUTTON_FILE_PATH + "button_cylinder_advance.png"
}
CYRINDER_RETRACTION_BUTTON_STATUS = {
    "coordinate" : (1100,490),
    "size"       : (550, 250),
    "image_path" : BUTTON_FILE_PATH + "button_cylinder_retraction.png"
}
PUMP_BUTTON_STATUS                = {
    "coordinate" : (350, 790),
    "size"       : (550, 250),
    "image_path" : BUTTON_FILE_PATH + "button_pump.png"
}
AIR_BLOW_BUTTON_STATUS            = {
    "coordinate" : (1100,790),
    "size"       : (550, 250),
    "image_path" : BUTTON_FILE_PATH + "button_air.png"
}
# 画像の設定
CATCH_EXPTXT_STATUS = {
    "coordinate" : (50,  220),
    "size"       : (400, 200),
    "image_path" : EXPTXT_FILE_PATH + "exptxt_catch.png"
}
WORK_EXPTXT_STATUS  = {
    "coordinate" : (500, 220),
    "size"       : (400, 200),
    "image_path" : EXPTXT_FILE_PATH + "exptxt_catch.png"
}
# ランプの設定
CATCH_LAMP_STATUS = {
    "x"     : 380,
    "y"     : 295,
    "w"     : 50,
    "h"     : 50,
    "color" : GRAY
    }
WORK_LAMP_STATUS  = {
    "x"      : 825,
    "y"      : 295,
    "w"      : 50,
    "h"      : 50,
    "color"  : GRAY
    }

TERMINATION = "動作完了"

WORK_LAMP  = "work"
CATCH_LAMP = "catch"

class WashScreen(BaseScreen):
    def __init__(self, screen: pygame.Surface, serial : PCManager):
        super().__init__(screen)
        self.serial = serial
        self.setting_lamps()

    # ボタンを生成
    def setting_buttons(self):
        self.buttons = [
            Button(self.screen, **BACK_BOTTON_STATUS, func=self.move_motion)
        ]
        self.lamp_buttons = [
            LampButton(self.screen, **ECCENTRICITY_BUTTON_STATUS,        func=self.test_eccentricity),
            LampButton(self.screen, **CYRINDER_ADVANCE_BUTTON_STATUS,    func=self.test_cylinder_advance),
            LampButton(self.screen, **CYRINDER_RETRACTION_BUTTON_STATUS, func=self.test_cylinder_retraction),
            LampButton(self.screen, **PUMP_BUTTON_STATUS,                func=self.test_pump),
            LampButton(self.screen, **AIR_BLOW_BUTTON_STATUS,            func=self.test_air_blow)
        ]
    
    # 画像を生成
    def setting_images(self):
        self.images = [
            Picture(self.screen, **WASH_TITLE_STATUS),
            Picture(self.screen, **CATCH_EXPTXT_STATUS),
            Picture(self.screen, **WORK_EXPTXT_STATUS)
        ]

    # ランプを生成
    def setting_lamps(self):
        self.lamps = {
            WORK_LAMP  : Lamp(self.screen, **CATCH_LAMP_STATUS),
            CATCH_LAMP : Lamp(self.screen, **WORK_LAMP_STATUS)
        }

    # 描画
    def draw(self):
        super().draw()
        for button in self.lamp_buttons:
            button.draw()
        message = self.serial.read()
        for key   in self.lamps:
            if message == "ワーク検知" and key == WORK_LAMP:
                self.lamps[key].update_color(GREEN)
            elif message == "引っかかり検知" and key == CATCH_LAMP:
                self.lamps[key].update_color(GREEN)
            else:
                self.lamps[key].update_color(YELLOW)
            self.lamps[key].draw()

    # 押下処理
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
    
    def test_eccentricity(self):
        return "処理に対応するkeyを返す", True

    def test_cylinder_advance(self):
        return "処理に対応するkeyを返す", True

    def test_cylinder_retraction(self):
        return "処理に対応するkeyを返す", True

    def test_pump(self):
        return "処理に対応するkeyを返す", True

    def test_air_blow(self):
        return "処理に対応するkeyを返す", True