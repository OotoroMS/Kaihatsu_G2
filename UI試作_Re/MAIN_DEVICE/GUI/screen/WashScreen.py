# 動作確認画面(投入・洗浄部)
import pygame
# 基本画面
from GUI.screen.BaseScreen import BaseScreen
# 部品
from GUI.parts.Button       import Button
from GUI.parts.Picture      import Picture
from GUI.parts.ButtonAtLamp import ButtonAtLamp as LampButton
from GUI.parts.Lamp         import Lamp
# 定数
from GUI.constant.screen.wash_constant      import *
from GUI.constant.screen_name               import *
from GUI.constant.color                     import *
# シリアル通信クラス
from SERIAL.manager.SerialUIBridge  import SerialUIBridge

class WashScreen(BaseScreen):
    def __init__(self, screen: pygame.Surface, serial : SerialUIBridge):
        super().__init__(screen)
        self.serial = serial
        self.setting_lamps()

    # ボタンを生成
    def setting_buttons(self):
        self.buttons = [
            Button(self.screen, **BACK_BOTTON_STATUS, func=self.move_motion)
        ]
        self.motion_Lamp_buttons = [
            LampButton(self.screen, **CYRINDER_ADVANCE_BUTTON_STATUS,    func=self.test_cylinder_advance),      # シリンダ前進
            LampButton(self.screen, **CYRINDER_RETRACTION_BUTTON_STATUS, func=self.test_cylinder_retraction)    # シリンダ後退
        ]
        self.motion_buttons      = [
            Button(self.screen, **ECCENTRICITY_BUTTON_STATUS, func=self.test_eccentricity), # 偏心モータ回転
            Button(self.screen, **PUMP_BUTTON_STATUS,         func=self.test_pump),         # ポンプ動作
            Button(self.screen, **AIR_BLOW_BUTTON_STATUS,     func=self.test_air_blow)      # エアブロー動作
        ]
    # 画像を生成
    def setting_images(self):
        self.images = [
            Picture(self.screen, **WASH_TITLE_STATUS),
            Picture(self.screen, **CATCH_EXPTXT_STATUS),    # 引っかかり検知
            Picture(self.screen, **WORK_EXPTXT_STATUS)      # ワーク検知
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
        for button in self.motion_Lamp_buttons:
            button.draw()
        for button in self.motion_buttons:
            button.draw()
        message = self.serial.process_serial_queue()
        for key   in self.lamps:
            if message[0][0] == "ワーク検知"    and key == WORK_LAMP:
                self.lamps[key].update_color(GREEN)
            if message[0][0] == "引っかかり検知" and key == CATCH_LAMP:
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
        for button in self.motion_Lamp_buttons:
            result,normal = button.is_clicked(event)
            if normal:
                self.lamp_button_clicked(button, result)
                return result, normal
        for button in self.motion_buttons:
            result, normal = button.is_clicked(event)
            if normal:
                self.button_clicked(result)
        return result, normal
    
    # ランプつきボタンの処理
    def lamp_button_clicked(self, button, result):
        self.serial.send_set(WASH_SCREEN_COMMAND[result])
        if type(button) == LampButton:
            button.update_lamp_color(GREEN)
        while True:
            button.draw()
            pygame.display.update()
            messege = self.serial.process_serial_queue()
            if messege and messege[0][0] == TERMINATION:
                button.update_lamp_color(YELLOW)
                break
            elif messege:   #   動作終了かどうか比較したほうが良いかも
                button.update_lamp_color(RED)
        button.draw()
        pygame.display.update()

    # 通常ボタンの処理
    def button_clicked(self, result):
        self.serial.send_set(WASH_SCREEN_COMMAND[result])
        while True:
            messege = self.serial.process_serial_queue()
            if messege: 
                break

    # 動作選択画面に戻る
    def move_motion(self):
        return MOTION, OK
    
    def test_eccentricity(self):
        return "eccentricity", True

    def test_cylinder_advance(self):
        return "cylinder_advance", True

    def test_cylinder_retraction(self):
        return "cylinder_retraction", True

    def test_pump(self):
        return "pump", True

    def test_air_blow(self):
        return "air_blow", True