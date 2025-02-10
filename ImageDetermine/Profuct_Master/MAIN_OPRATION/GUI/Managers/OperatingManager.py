# 稼働状況管理
import pygame
import SERIAL.serial_gate
# 定数
from MAIN_OPRATION.GUI.Constants.operation_status           import *
from MAIN_OPRATION.GUI.Constants.opratingmanager_constant   import *
from MAIN_OPRATION.GUI.Constants.file_path                  import *
from MEINTENANCE.GUI.constants.popup_name                   import *

class OperatingManager:
    def __init__(self, screen : pygame.Surface, serial : SERIAL.serial_gate.SerialGate) -> None:
        # 対象の画面
        self.screen = screen
        # シリアル通信クラス(受信のみ)
        self.serial = serial
        # 稼働状況保持変数
        self.oprating_status = b'241'
        self.oprating_text   = OPERATION_STOP
        # 表示領域生成
        self.rect = pygame.rect.Rect(RECT_X, RECT_Y, RECT_WIDTH, RECT_HEIGHT)
        # 表示フォント
        self.font = pygame.font.Font(FONT, FONT_SIZE)
    
    def receive_operating_status(self):
        self.oprating_status = self.serial.get_receive_data()
    
    def status_check(self):
        if self.oprating_status:
            if self.oprating_status == STOP_STATUS:
                self.oprating_text = OPERATION_STOP
                return True
            elif self.oprating_status in ERROR_STATUS:
                self.oprating_text = OPERATION_ERROR
                return True
            elif self.oprating_status in OPERATION_ACTIVE:
                self.oprating_text = OPERATION_ACTIVE
                return True
        return True
    
    def draw(self):
        try:
            veiw_status = self.font.render(self.oprating_text, True, BLACK)
            pygame.draw.rect(self.screen, BACK_COROR[self.oprating_text], self.rect)    # 表示領域
            pygame.draw.rect(self.screen, BLACK,                          self.rect, 1) # 外枠  
            veiw_xy = veiw_status.get_rect(center=self.rect.center)
            self.screen.blit(veiw_status, veiw_xy)
            return True
        except Exception as e:
            print(e)
            return False
    
    # 受信及び描画処理
    def status_receve_draw(self) -> bool:
        self.receive_operating_status()
        if not self.status_check():
            # print("OOperatingMaanager.py status_receve_draw : ｽﾃｰﾀｽｴﾗｰ")
            return False
        if not self.draw():
            # print("OOperatingMaanager.py status_receve_draw : 描画失敗")
            return False
        # print("OOperatingMaanager.py status_receve_draw : 描画成功")
        return True

    def foward_error(self):
        if self.oprating_text == OPERATION_ERROR:
            error = [self.oprating_text, "外観検査"]
            return True, ERROR_POPUP, error
        return False, None, [None, None]