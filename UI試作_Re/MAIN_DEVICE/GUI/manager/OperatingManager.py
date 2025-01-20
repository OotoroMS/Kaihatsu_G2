# 稼働状況表示管理
import pygame
import queue
# シリアル通信
from SERIAL.manager.SerialUIBridge  import SerialUIBridge
# 定数
from GUI.constant.file_path        import *
from GUI.constant.operating_status import *
from GUI.constant.popup_name       import *
from GUI.constant.color            import *

VIEW_RECT = ((1410, 10, 500, 160))
RECT_X      = 1410
RECT_Y      = 10
RECT_WIDTH  = 500
RECT_HEIGHT = 160
FONT_SIZE   = 30

BACK_COROR = {
    STATUS_ACTIVE : GREEN,
    STATUS_STOP   : YELLOW,
    STATUS_ERROR  : RED
}

class OperatingManager:
    def __init__(self, screen : pygame.Surface, serial : SerialUIBridge, send_que : queue.Queue, recv_que : queue.Queue) -> None:
        self.screen = screen
        self.serial = serial
        self.recv_que = recv_que
        self.send_que = send_que
        # 表示領域生成
        self.rect = pygame.rect.Rect(RECT_X, RECT_Y, RECT_WIDTH, RECT_HEIGHT)
        # 表示フォント
        self.font = pygame.font.Font(FONT, FONT_SIZE)
        # 稼働状況とｴﾗｰ発生場所
        # self.operating_status = ""
        self.operating_status = STATUS_STOP # デバック用
        self.plase            = "洗浄部"
        # 表示テキスト
        self.text = STATUS_STOP

    # 稼働状況を受け取る
    def receive_operating_status(self) -> bool:
        if self.operating_status == STATUS_STOP or STATUS_ERROR:
            message = self.serial.process_serial_queue()
        elif self.operating_status == STATUS_ACTIVE:
            if not self.recv_que.empty():
                message = self.recv_que.get()
        if message[0] != None:
            self.operating_status = message[0][0]
            self.plase            = message[0][1]
            self.send_que.put(self.operating_status)
            # print("self.operating_status :", self.operating_status)
            # print("self.plase            :", self.plase)
            return True
        else:
            # print("self.operating_status :", self.operating_status)
            # print("self.plase            :", self.plase)
            return True
        return False
    
    # 受け取った稼働状況を判別
    def status_check(self) -> bool:
        if self.operating_status[:3]   == STATUS_ERROR:
            self.text = STATUS_ERROR
            return True
        elif self.operating_status[:3] == STATUS_ACTIVE:
            self.text = STATUS_ACTIVE
            return True
        elif self.operating_status[:3] == STATUS_STOP:
            self.text = STATUS_STOP
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
    def status_receve_draw(self, tcnt : int) -> bool:
        if not self.receive_operating_status():
            return False
        if not self.status_check():
            print("not status_check")
            return False
        if not self.draw():
            return False
        return True
        
    
    def foward_error(self):
        if self.operating_status:
            if self.operating_status[:3] == STATUS_ERROR:
                return True, ERROR_POPUP, [self.operating_status, self.plase]
            else:
                return False, None, None
        else:
                return False, None, None
        # デバック用
        # if self.operating_status == STATUS_ERROR:
        #     error = [self.operating_status + "001", self.plase]
        #     return True, ERROR_POPUP, error
        # else:
        #     return False, None, None
    