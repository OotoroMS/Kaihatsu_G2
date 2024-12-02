# パスワード変更画面
from pygame import Surface
from GUI.screen.PassScreen                      import *
from GUI.constant.screen.change_pass_constant   import *


class ChangePassScreen(PassScreen):
    def __init__(self, screen: Surface):
        super().__init__(screen)
        self.progress_pass = NEW    # 変更作業の進行度(初期はNEW)
        self.new_password  = ""
    
    def setting_images(self):
        super().setting_images()
        self.images[TITLE] = Picture(self.screen, **PASS_TITLE_STATUS)
        self.gaid_images = {
            NEW   : Picture(self.screen, **NEW_PASSWORD_EXPTXT_STAUTS),
            RETRY : Picture(self.screen, **RETRY_PASSWORD_EXPTXT_STATUS)
        }

    def draw(self):
        super().draw()
        self.gaid_images[self.progress_pass].draw()
    
        # enterの処理
    def num_check(self):
        if not self.set_pass:
            return RPASS_POPUP, OK  # 入力促進POPUPを表示
        # 再入力なら
        elif self.progress_pass == RETRY:
            return self.pass_check()
        # 初回なら
        elif self.progress_pass == NEW:
            self.new_password  = self.set_pass
            self.progress_pass = RETRY
            self.set_pass      = ""
            return None, OK
        return None, False

    # 再入力判定処理
    def pass_check(self):
        if self.set_pass == self.new_password:
            query = QUERY + self.new_password
            self.db.db_query_execution(DATABESE, query)
            self.progress_pass = NEW
            self.set_pass = ""
            return SPASS_POPUP, OK   # 変更成功POPUP画面を表示
        else:
            self.set_pass = ""
            self.progress_pass = NEW
            return EPASS_POPUP, OK   # 最初からやり直すPOPUP画面を表示

    def move_screen(self):
        return MOTION, OK