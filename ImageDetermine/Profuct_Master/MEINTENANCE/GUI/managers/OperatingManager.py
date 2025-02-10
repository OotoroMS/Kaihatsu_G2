# 稼働状況表示管理
import pygame
# 定数(全体)
from MEINTENANCE.CONSTANTS.operation_status import *
# 定数(UI)
from MEINTENANCE.GUI.constants.file_path    import *
from MEINTENANCE.GUI.constants.popup_name   import *
from MEINTENANCE.GUI.constants.color        import *

VIEW_RECT = ((1410, 10, 500, 160))
RECT_X      = 1410
RECT_Y      = 10
RECT_WIDTH  = 500
RECT_HEIGHT = 160
FONT_SIZE   = 30

BACK_COROR = {
    OPERATION_ACTIVE : GREEN,
    OPERATION_STOP   : YELLOW,
    OPERATION_ERROR  : RED
}

class OperatingManager:
    def __init__(self, screen : pygame.Surface) -> None:
        self.screen = screen
        # 表示領域生成
        self.rect = pygame.rect.Rect(RECT_X, RECT_Y, RECT_WIDTH, RECT_HEIGHT)
        # 表示フォント
        self.font = pygame.font.Font(FONT, FONT_SIZE)
        # 稼働状況とｴﾗｰ発生場所
        # self.operating_status = ""
        self.operating_status = OPERATION_ERROR # デバック用
        self.plase            = "洗浄部"
        # 表示テキスト
        self.text = OPERATION_ERROR

    # 稼働状況を受け取る
    def receive_operating_status(self, message : tuple[str, str]) -> bool:
        if message:
            self.operating_status = message[0]
            self.plase            = message[1]
            return True
        return False
    
    # 受け取った稼働状況を判別
    def status_check(self) -> bool:
        if self.operating_status[:3]   == OPERATION_ACTIVE:
            self.text = OPERATION_ACTIVE
            return True
        elif self.operating_status[:3] == OPERATION_STOP:
            self.text = OPERATION_STOP
            return True
        elif self.operating_status[:3] == OPERATION_ERROR:
            self.text = OPERATION_ERROR
            return True
        return False
    
    # 描画
    def draw(self) -> bool:
        try:
            veiw_status = self.font.render(self.text, True, BLACK)
            pygame.draw.rect(self.screen, BACK_COROR[self.text], self.rect)    # 表示領域
            pygame.draw.rect(self.screen, BLACK,                 self.rect, 1) # 外枠  
            veiw_xy = veiw_status.get_rect(center=self.rect.center)
            self.screen.blit(veiw_status, veiw_xy)
            return True
        except Exception as e:
            print(e)
            return False

    # 受信及び描画処理
    def status_receve_draw(self, status : tuple[str, str]) -> bool:
        self.receive_operating_status(status)
        if not self.status_check():
            # print("OOperatingMaanager.py status_receve_draw : ｽﾃｰﾀｽｴﾗｰ")
            return False
        if not self.draw():
            # print("OOperatingMaanager.py status_receve_draw : 描画失敗")
            return False
        # print("OOperatingMaanager.py status_receve_draw : 描画成功")
        return True
    
    def foward_error(self):
        # デバック用
        if self.operating_status[:3] == OPERATION_ERROR:
            error = [self.operating_status + "001", self.plase]
            # error = [self.operating_status, self.plase]
            return True, ERROR_POPUP, error
        else:
            return False, None, None
    