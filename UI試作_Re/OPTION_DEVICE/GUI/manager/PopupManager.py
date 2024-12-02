import pygame
# 定数
from GUI.constant.popup.popup_name import *
from GUI.constant.judge_result     import *
# POPUPクラス
from GUI.popup.TextPopup  import TextPopup
from GUI.popup.EndPopup   import EndPopup
from GUI.popup.PassPopup  import PassPopup
from GUI.popup.ResetPopup import ResetPopup
from GUI.popup.ErrorPopup import ErrorPopup
class PopupManager:
    def __init__(self, screen : pygame.Surface) -> None:
        self.screen = screen
        self.popups = {
            NONE_DATA   : TextPopup(self.screen, NONE_DATA),
            DB_RESET    : TextPopup(self.screen, DB_RESET),
            INDICATOR_OK: TextPopup(self.screen, INDICATOR_OK),
            INDICATOR_NG: TextPopup(self.screen, INDICATOR_NG),
            END_POPUP   : EndPopup(self.screen, END_POPUP),
            PASS_POPUP  : PassPopup(self.screen, PASS_POPUP1, PASS_POPUP2),
            EPASS_POPUP : PassPopup(self.screen, PASS_POPUP1, PASS_POPUP3),
            SPASS_POPUP : TextPopup(self.screen, SPASS_POPUP),
            RPASS_POPUP : TextPopup(self.screen, RPASS_POPUP),
            RESET_ASK   : ResetPopup(self.screen, RESET_ASK),
            ERROR_POPUP : ErrorPopup(self.screen, ERROR_POPUP)
        }
    
    # POPUP描画
    def popup_draw(self, popup_name : str):
        popup = self.popup_check(popup_name)
        if popup:
            popup.draw()
            return SUCCESS
        else:
            return FAILURE
    
    # キーに対応したPOPUPがあれば返す。ない場合はNoneを返す。
    def popup_check(self, key):
        if key in self.popups.keys():
            return self.popups[key]
        return None
    
     # イベントが発生したか確認
    def popup_event_check(self, popup_name):
        result = None
        normal = FAILURE
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
    
    # # エラーポップの表示内容を更新
    # def set_error_popup(self, error : tuple[str, str]):
    #     self.popups[ERROR_POPUP].error_update(error)