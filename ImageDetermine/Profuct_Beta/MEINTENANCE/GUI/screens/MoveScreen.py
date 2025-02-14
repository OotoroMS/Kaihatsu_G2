import pygame
from pygame.event import Event
# 定数(全体)
from MEINTENANCE.CONSTANTS.command_type     import *
from MEINTENANCE.CONSTANTS.command          import *
from MEINTENANCE.CONSTANTS.serial_result    import *
import MEINTENANCE.CONSTANTS.move_moter_pos as MOVE_MOTOR_POS
# 定数
from MEINTENANCE.GUI.constants.screen_configs.move_config   import *
from MEINTENANCE.GUI.constants.button_result                import *
from MEINTENANCE.GUI.constants.screen_name                  import *
from MEINTENANCE.GUI.constants.file_path                    import *
from MEINTENANCE.GUI.constants.color                        import *
# 部品
from MEINTENANCE.GUI.parts.ButtonAtLamp import ButtonAtLamp as LampButton
from MEINTENANCE.GUI.parts.Picture      import Picture
from MEINTENANCE.GUI.parts.Button       import Button
from MEINTENANCE.GUI.parts.Lamp         import Lamp
# 基本クラス
from MEINTENANCE.GUI.screens.BaseScreen  import BaseScreen


class MoveScreen(BaseScreen):
    def __init__(self, screen: pygame.Surface) -> None:
        super().__init__(screen)
        self.setting_lamps()
        self.move_lamp_point = 1
        self.show_adsorption = BUTTON_ON
        self.in_work  = b'\xd0\n'
        self.out_work = b'\xce\n'
        self.move_pos = None

    def setting_buttons(self):
        self.buttons = [
            Button(self.screen, **BOTTON_BACK_STATUS,          func=self.back)
        ]
        self.pless_buttons = [
            Button(self.screen, **BOTTON_MOTOR_NOMAL_STATUS,   func=self.motor_nomal),
            Button(self.screen, **BUTTON_MOTOR_REVERSE_STATUS, func=self.motor_reverse)
        ]
        self.lamp_buttons = [
            LampButton(self.screen, **BUTTON_CYLINDER_UP_STATUS,   func=self.cylinder_up),
            LampButton(self.screen, **BUTTON_CYLINDER_DOWN_STATUS, func=self.cylinder_down)
        ]
        self.absorption_buttons = [
            LampButton(self.screen, **BUTTON_ADSORPTION_STATUS, func=self.absorption_on),
            LampButton(self.screen, **BUTTON_ADSORPTION_STATUS, func=self.absorption_off)
        ]
        self.absorption_buttons[BUTTON_ON].update_lamp_color(GRAY)
        self.absorption_buttons[BUTTON_OFF].update_lamp_color(GREEN)

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
        
    
    def draw_buttons(self):
        super().draw_buttons()
        for button in self.lamp_buttons:
            button.draw()
        for button in self.pless_buttons:
            button.draw()
        self.absorption_buttons[self.show_adsorption].draw()

    def draw_lamps(self):
        for lamp in self.motor_lamps:
            lamp.draw()
        self.work_lamp_update()
        for lamp in self.work_lamps:
            lamp.draw()
    
    def clicked(self, event: Event):
        result = None
        normal = False
        cnt = 0
        for button in self.buttons:
            if type(button) == Button:
                result, normal = button.is_clicked(event)
            if normal:
                return result, normal
        for button in self.lamp_buttons:
            if type(button) == LampButton:
                result, normal = button.is_clicked(event)
            if normal:
                return result, normal
        for button in self.pless_buttons:
            result, normal = button.is_pressed(event)
            if normal:
                return result, normal
        result, normal = self.absorption_buttons[self.show_adsorption].is_clicked(event)
        return result, normal

    def lamp_update_green(self, key):
        if key in CYLINDER_RESULT.keys():
            button_index = CYLINDER_RESULT[key]
            for i in range(len(self.lamp_buttons)):
                if i == button_index:
                    self.lamp_buttons[i].update_lamp_color(GREEN)
                else:
                    self.lamp_buttons[i].update_lamp_color(GRAY)
            self.draw_buttons()
            pygame.display.update()

    def lamp_update_yellow(self, key):
        if key in CYLINDER_RESULT.keys():
            button_index = CYLINDER_RESULT[key]
            for i in range(len(self.lamp_buttons)):
                if i == button_index:
                    self.lamp_buttons[i].update_lamp_color(YELLOW)
                else:
                    self.lamp_buttons[i].update_lamp_color(GRAY)
            self.draw_buttons()
            pygame.display.update()

    def work_lamp_update(self):
        if self.in_work == IN_WORK_ON_STAUTS:
            self.work_lamps[0].update_color(GREEN)
        elif self.in_work == IN_WORK_OFF_STAUTS:
            self.work_lamps[0].update_color(GRAY)
        if self.out_work == OUT_WORK_ON_STAUTS:
            self.work_lamps[1].update_color(GREEN)
        elif self.out_work == OUT_WORK_OFF_STAUTS:
            self.work_lamps[1].update_color(GRAY)
        # if key in WORK_RESULT.keys():
        #     lump_index = WORK_RESULT[key]
        #     for i in range(len(self.work_lamps)):
        #         if i == lump_index:
        #             self.work_lamps[i].update_color(GREEN)
        #         else:
        #             self.work_lamps[i].update_color(GRAY)
        # else:
        #     for lamp in self.work_lamps:
        #         lamp.update_color(GRAY)

    def work_status_update(self, key : list):
        if len(key) >= 2:
            self.in_work  = key[0]
            self.out_work = key[1]
            # print("MoveScreen.py work_status_update : in_work is ", self.in_work)
            # print("MoveScreen.py work_status_update : out_work is ", self.out_work)


    def move_lamp_update(self, opration : str, command : str):
        color = GRAY
        if opration in MOVE_MOTOR_POS.MOTOR_POS_LIST:
            move_pos = MOVE_MOTOR_POS.MOTOR_POS_LAMP_DICT[opration]
            if move_pos == 0 or move_pos == 5:
                color = RED
            else:
                color = GREEN
            for i in range(len(self.motor_lamps)):
                if i == move_pos:
                    self.motor_lamps[i].update_color(color)
                else:
                    self.motor_lamps[i].update_color(GRAY)
                
        
        # if opration == RUN:
        #     color = GREEN
        # if opration == FINISH:
        #     color = YELLOW
        #     if command == MOTOR_NOMAL and self.move_lamp_point < 5:
        #         self.move_lamp_point += 1
        #     elif command == MOTOR_REVERSE and self.move_lamp_point > 0:
        #         self.move_lamp_point -= 1
        # if self.move_lamp_point <= 0 or self.move_lamp_point >= 5:
        #     color = RED
        # for i in range(len(self.motor_lamps)):
        #     if i == self.move_lamp_point:
        #         self.motor_lamps[i].update_color(color)
        #     else:
        #         self.motor_lamps[i].update_color(GRAY)
        self.draw_lamps()
        pygame.display.update()
    
    # 戻るボタン
    def back(self):
        return MAIN, PRESS
    
    # 正転
    def motor_nomal(self):
        return MOTOR_NOMAL, PRESS
    
    # 反転
    def motor_reverse(self):
        return MOTOR_REVERSE, PRESS
    
    def cylinder_up(self):
        return CYLINDER_UP_START, PRESS
    
    def cylinder_down(self):
        return CYLINDER_DOWN_START, PRESS
    
    def absorption_on(self):
        self.show_adsorption = BUTTON_OFF
        return ADSORPTION_ON, PRESS
    
    def absorption_off(self):
        self.show_adsorption = BUTTON_ON
        return ADSORPTION_OFF, PRESS