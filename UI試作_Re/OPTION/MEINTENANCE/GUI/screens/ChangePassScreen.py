# パスワード変更画面
from pygame import Surface
from MEINTENANCE.GUI.screens.BaseScreen                             import *
# 定数(全体)
from MEINTENANCE.CONSTANTS.command_type    import *
# 定数(GUI)
from MEINTENANCE.GUI.constants.screen_configs.change_pass_config    import *
from MEINTENANCE.GUI.constants.screen_name                          import *
from MEINTENANCE.GUI.constants.popup_name                           import *
from MEINTENANCE.GUI.constants.color                                import *

class ChangePassScreen(BaseScreen):
    def __init__(self, screen : pygame.Surface):
        super().__init__(screen)
        self.mode = NEW
        self.set_pass = ""
        self.new_pass = ""
        self.pass_font = pygame.font.Font(FONT, PASS_FONT_SIZE)
        self.pass_rect = pygame.rect.Rect(660, 200, 600, 170)

    def create_func_list(self):
        self.func_list = [
            self.num_1,
            self.num_2,
            self.num_3,
            self.num_4,
            self.num_5,
            self.num_6,
            self.num_7,
            self.num_8,
            self.num_9
        ]

    def setting_buttons(self):
        self.create_func_list()
        self.buttons = [
            Button(self.screen, **BACK_BOTTON_STATUS, func=self.move_screen),
            Button(self.screen, **CLR_BUTTON_STATUS,  func=self.num_clr),
            Button(self.screen, **ENT_BUTTON_STATUS,  func=self.num_check),
            Button(self.screen, **ZERO_BUTON_STATUS,  func=self.num_0)
        ]
        self.buttons[3].off_hover_flag()
        func_index = 0
        for y in range(0,3):
            for x in range(0,3):
                button = Button(self.screen, (NUM_BUTTONS_X[x], NUM_BUTTONS_Y[y]), NUM_BUTTONS_SIZE,NUM_BUTTONS_FILE_PATH[func_index], self.func_list[func_index])
                button.off_hover_flag()
                self.buttons.append(button)
                func_index += 1

    def setting_images(self):
        self.images = [
            Picture(self.screen, **PASS_TITLE_STATUS),
            Picture(self.screen, **ROCK_EXPEXT_STATUS)
        ]
        self.gaid_images = {
            NEW   : Picture(self.screen, **NEW_PASSWORD_EXPTXT_STAUTS),
            RETRY : Picture(self.screen, **RETRY_PASSWORD_EXPTXT_STATUS)
        }


    def draw(self):
        for image in self.images:
            image.draw()
        self.draw_pass()
        for button in self.buttons:
            button.draw()
        self.gaid_images[self.mode].draw()

    def draw_pass(self):
        self.passward = self.pass_font.render(self.set_pass, True, BLACK)
        self.pass_center = self.passward.get_rect(center=self.pass_rect.center)
        pygame.draw.rect(self.screen, (255,255,255), self. pass_rect)   #   稼働状況更新の領域を確保
        pygame.draw.rect(self.screen, BLACK, self.pass_rect, 5)         #   外枠を描画
        self.screen.blit(self.passward,self.pass_center)

    def num_0(self):
        if len(self.set_pass) <= PASSINPUTMAX:
            self.set_pass += "0"
        return None, True
    def num_1(self):
        if len(self.set_pass) <= PASSINPUTMAX:
            self.set_pass += "1"
        return None, True
    def num_2(self):
        if len(self.set_pass) <= PASSINPUTMAX:
            self.set_pass += "2"
        return None, True
    def num_3(self):
        if len(self.set_pass) <= PASSINPUTMAX:
            self.set_pass += "3"
        return None, True
    def num_4(self):
        if len(self.set_pass) <= PASSINPUTMAX:
            self.set_pass += "4"
        return None, True
    def num_5(self):
        if len(self.set_pass) <= PASSINPUTMAX:
            self.set_pass += "5"
        return None, True
    def num_6(self):
        if len(self.set_pass) <= PASSINPUTMAX:
            self.set_pass += "6"
        return None, True
    def num_7(self):
        if len(self.set_pass) <= PASSINPUTMAX:
            self.set_pass += "7"
        return None, True
    def num_8(self):
        if len(self.set_pass) <= PASSINPUTMAX:
            self.set_pass += "8"
        return None, True
    def num_9(self):
        if len(self.set_pass) <= PASSINPUTMAX:
            self.set_pass += "9"
        return None, True
    
    def num_clr(self):
        self.set_pass = ""
        return None, True
    
    def move_screen(self):
        return MAIN, True
    
    def num_check(self):
        if self.set_pass:
            return self.check_pass()
        else:
            return RPASS_POPUP, True
    
    def check_pass(self):
        if self.mode == RETRY and self.set_pass == self.new_pass:
            print("update")
            new_pass = UPDATE_PASS + self.set_pass
            self.set_pass = ""
            self.mode     = NEW
            return new_pass, True
        elif self.mode == RETRY:
            self.mode     = NEW
            self.set_pass = ""
            return RETRY_POPUP, True
        elif self.mode == NEW:
            self.new_pass = self.set_pass
            self.set_pass = ""
            self.mode = RETRY
            return None, True
        return None, False

    