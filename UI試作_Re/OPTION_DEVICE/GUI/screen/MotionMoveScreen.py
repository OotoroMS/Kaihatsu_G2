import pygame
# 定数
from GUI.constant.file_path                     import *
from GUI.constant.judge_result                  import *
from GUI.constant.color                         import *
from GUI.constant.screen.motion_move_constant   import *
from GUI.constant.screen.screen_name            import *
from GUI.constant.popup.popup_name              import *
# 部品
from GUI.parts.Button       import Button
from GUI.parts.Picture      import Picture
from GUI.parts.ButtonAtLamp import ButtonAtLamp as LampButton
from GUI.parts.Lamp         import Lamp
# 基本クラス
from GUI.screen.BaseScreen  import BaseScreen
# シリアル通信用クラス
from SERIAL.pc_comands  import *

class MotionMoveScreen(BaseScreen):
    def __init__(self, screen: pygame.Surface, serial : PCManager) -> None:
        super().__init__(screen)
        self.setting_lamps()
        self.serial = serial
    
    def setting_buttons(self):
        self.buttons = [
            Button(self.screen, **BOTTON_BACK_STATUS,          func=self.back),
            Button(self.screen, **BOTTON_MOTOR_NOMAL_STATUS,   func=None),
            Button(self.screen, **BUTTON_MOTOR_REVERSE_STATUS, func=None),
            Button(self.screen, **BUTTON_ADSORPTION_STATUS,    func=None)
        ]
        self.lamp_buttons = [
            LampButton(self.screen, **BUTTON_CYLINDER_UP_STATUS,   func=None),
            LampButton(self.screen, **BUTTON_CYLINDER_DOWN_STATUS, func=None)
        ]

    def setting_images(self):
        self.images = [
            Picture(self.screen, **TETLE_MOTION_STATUS),
            Picture(self.screen, **EXPTXT_LAMP_STATUS),
            Picture(self.screen, **EXPTXT_WORK_IN_STATUS),
            Picture(self.screen, **EXPTXT_WORK_OUT_STATUS)
        ]

    # ランプ
    def setting_lamps(self):
        self.motor_lamps = [
            Lamp(self.screen, **LAMP_MOTOR_LEFT_LIMIT),
            Lamp(self.screen, **LAMP_MOTOR_01),
            Lamp(self.screen, **LAMP_MOTOR_02),
            Lamp(self.screen, **LAMP_MOTOR_03),
            Lamp(self.screen, **LAMP_MOTOR_04),
            Lamp(self.screen, **LAMP_MOTOR_RIGHT_LIMIT)
        ]
        self.work_lamps = [
            Lamp(self.screen, **LAMP_CYLINDER_UP),
            Lamp(self.screen, **LAMP_CYLINDER_DOWN)
        ]

    # 画面を描画
    def draw(self):
        super().draw()
        self.draw_lamps()

    # ボタンを描画    
    def draw_buttons(self):
        super().draw_buttons()
        for button in self.lamp_buttons:
            button.draw()

    # ランプを描画
    def draw_lamps(self):
        for lamp in self.motor_lamps:
            lamp.draw()
        for lamp in self.work_lamps:
            lamp.draw()

    def clicked(self, event):
        result = None
        normal = FAILURE
        # ボタンの判定
        result, normal = self.button_clicked(event)
        if normal:
            return result, normal
        # ランプ付きボタンの判定
        result, normal, button = self.lamp_button_clicked(event)
        if normal:
            self.lamp_button_clicked(self, button, result)
            return result, normal
        return result, normal

    def lamp_button_clicked(self, button, result):
        self.serial.write_serial("辞書型コマンド[result]")
        if type(button) == LampButton:
            button.update_lamp_color(YELLOW)
        while True:
            button.draw()
            pygame.display.update()
            messege = self.serial.read()
            if messege and messege == TERMINATION:
                break
        if type(button) == LampButton:
            button.update_lamp_color(GREEN)
        button.draw()
        pygame.display.update()


    # ボタンの判定
    def button_clicked(self, event):
        result = None
        normal = FAILURE
        for button in self.buttons:
            result, normal = button.is_clicked(event)
            if normal:
                return result, normal
        return result, normal

    # ランプ付きボタンの判定
    def lamp_button_clicked(self, event):
        for lamp_button in self.lamp_buttons:
            result, normal = lamp_button.is_clicked(event)
            if normal:
                return result, normal, lamp_button
        return result, normal, None

    # 戻るボタン
    def back(self):
        return MOTION, SUCCESS
