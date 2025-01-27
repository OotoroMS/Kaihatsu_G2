import pygame
# 定数
from MEINTENANCE.GUI.constants.file_path        import *
from MEINTENANCE.GUI.constants.popup_name       import *
from MEINTENANCE.GUI.constants.color            import *
# POPUP
from MEINTENANCE.GUI.popups.OperationPopup  import OperationPopup
from MEINTENANCE.GUI.popups.TextPopup       import TextPopup
from MEINTENANCE.GUI.popups.ResetPopup      import ResetPopup
from MEINTENANCE.GUI.popups.BackPopup       import BackPopup
from MEINTENANCE.GUI.popups.PassErrorPopup  import PassErrorPopup, RESET, RETRY
class PopupManager:
    def __init__(self, screen : pygame.Surface) -> None:
        self.screen = screen
        self.popups = {
            DB_RESET_POPUP   : ResetPopup(self.screen, DB_RESET_POPUP),
            SUCCESS_POPUP    : TextPopup(self.screen, SUCCESS_POPUP),
            CHANGE_POPUP     : TextPopup(self.screen, CHANGE_POPUP),
            RPASS_POPUP      : TextPopup(self.screen, RPASS_POPUP),
            BACK_POPUP       : BackPopup(self.screen),
            RETRY_POPUP      : PassErrorPopup(self.screen)
        }
    
    def popup_draw(self, popup_name : str):
        popup = self.popup_check(popup_name)
        if popup:
            popup.draw()
            return True
        return False
    
    # POPUPが登録されているか確認
    def popup_check(self, key):
        if key in self.popups.keys():
            return self.popups[key]
        return None
    
    # イベントが発生したか確認
    def popup_event_check(self, popup_name):
        result = None
        normal = False
        popup = self.popup_check(popup_name)
        if popup:
            result, normal = popup.click_event()
            return result, normal
        else:
            return result, normal

    # 渡されたキーが登録されているか確認
    def popup_search(self, key):
        if key in self.popups.keys():
            return True
        return False