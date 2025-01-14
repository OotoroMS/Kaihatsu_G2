# 動作確認画面(寸法部)
import pygame
# 基本画面
from GUI.screen.BaseScreen  import BaseScreen
# シリアル通信クラス
from SERIAL.manager.SerialUIBridge  import SerialUIBridge
# インジケータクラス
from DEGITALINDICATOR.Meas  import MeasurementConverter
# 部品
from GUI.parts.Button       import Button
from GUI.parts.Picture      import Picture
from GUI.parts.ButtonAtLamp import ButtonAtLamp as LampButton
from GUI.parts.Lamp         import Lamp
# 定数
from GUI.constant.file_path             import *
from GUI.constant.screen_name           import *
from GUI.constant.color                 import *
from GUI.constant.popup_name            import *
from GUI.constant.screen.meas_constant  import *
# データベース
from DATABASE.SQLCommunication import SQLCommunication

class MeasScreen(BaseScreen):
    def __init__(self, screen: pygame.Surface, serial : SerialUIBridge):
        super().__init__(screen)
        self.serial = serial
        self.db     = SQLCommunication()
    
    def setting_buttons(self):
        self.buttons = [
            Button(self.screen, **BACK_BOTTON_STATUS,      func=self.move_motion),
            Button(self.screen, **INDICATOR_BUTTON_STATUS, func=self.indicator_update)
        ]
        self.lamp_buttons = [
            LampButton(self.screen, **SORTING_FORWARD_BUTTON_STATUS, func=self.sorting_forward),
            LampButton(self.screen, **BUTTON_SORTING_BACK_STATUS,    func=self.sorting_back),
            LampButton(self.screen, **BUTTON_MEAS_BACK_STATUS,       func=self.meas_back),
            LampButton(self.screen, **MEAS_UP_BUTTON_STATUS,         func=self.meas_up),
            LampButton(self.screen, **MEAS_DOWN_BUTTON_STATUS,       func=self.meas_down),
        ]
        self.motion_buttons = [
            Button(self.screen, **MEAS_FORWARD_BUTTON_STATUS,    func=self.meas_forward)
        ]

    def setting_images(self):
        self.images = [
            Picture(self.screen, **MEAS_TITLE_STATUS)
        ]

    # 描画
    def draw(self):
        super().draw()
        for button in self.lamp_buttons:
            button.draw()
        for button in self.motion_buttons:
            button.draw()

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
        for button in self.motion_buttons:
            result, normal = button.is_clicked(event)
            if normal:
                self.button_clicked(event)
        return result, normal
    
    def lamp_button_clicked(self, button, result):
        self.serial.set_and_send(MEAS_COMAND[result])
        if type(button) == LampButton:
            button.update_lamp_color(YELLOW)
        while True:
            button.draw()
            pygame.display.update()
            messege = self.serial.process_serial_queue()
            if messege and messege[0] == TERMINATION:
                if type(button) == LampButton:
                    button.update_lamp_color(GREEN)
                if type(button) == LampButton:
                    button.update_lamp_color(RED)
                break
        button.draw()
        pygame.display.update()

    def button_clicked(self, result):
        self.serial.set_and_send(MEAS_COMAND[result])
        while True:
            messege = self.serial.process_serial_queue()
            if messege and messege[0] == TERMINATION:
                break    

    # 動作選択画面に戻る
    def move_motion(self):
        return MOTION, OK
  
    def indicator_update(self):
        return CHANGE_MEAS, True
    
    def meas_forward(self):
        return "処理に対応するkeyを返す", True
    
    def meas_back(self):
        return "処理に対応するkeyを返す", True
    
    def sorting_back(self):
        return "処理に対応するkeyを返す", True

    def sorting_forward(self):
        return "処理に対応するkeyを返す", True
    
    def meas_up(self):
        return "処理に対応するkeyを返す", True
    
    def meas_down(self):
        return "処理に対応するkeyを返す", True