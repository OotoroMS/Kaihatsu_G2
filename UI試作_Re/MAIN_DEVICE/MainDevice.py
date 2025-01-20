# 統括プログラムの予定
import pygame
import serial
import threading
import queue
# 自作モジュール
from GUI.application                import Application
from SERIAL.manager.SerialUIBridge  import SerialUIBridge
from DegitalIndicator               import DegitalIndicator
PORT1 = "COM3" # 適切なポートに変更してください
BAUD_RATE = 9600
TIMEOUT = 0.08
PARITY = serial.PARITY_EVEN
STOPBITS = serial.STOPBITS_ONE

SERIAL_PARAMS_GUI = {
    "port": "COM3",
    "baudrate": 9600,
    "parity": serial.PARITY_NONE,
    "stopbits": serial.STOPBITS_ONE,
    "timeout": 0.08
}

SERIAL_PARAMS_DE  = {
    "port"      : None,
    "baudrate"  : 2400,
    "parity"    : serial.PARITY_NONE,
    "stopbits"  : serial.STOPBITS_ONE,
    "timeout"   : 0.08
}
VAITAL = ["稼働中", "停止中", "エラー"]


class SerialRead:
    def __init__(self, serial : SerialUIBridge, oprating_recv_que : queue.Queue,oprating_send_que : queue.Queue, meas_que : queue.Queue):
        self.serial         = serial
        self.loop_flg       = True
        self.op_recv_que    = oprating_recv_que
        self.op_send_que    = oprating_send_que
        self.meas_que       = meas_que
        self.vaital         = "停止中"
    # 受信
    def read(self):
        while self.loop_flg:
            if not self.op_recv_que.empty():
                self.vaital = self.op_recv_que.get()
            self.serial.read_loop()
            if self.vaital == "稼働中":
                message = self.serial.process_serial_queue()
                if message[0][0] in VAITAL:
                    self.op_send_que.put(message)
                if message[0][0] == "取得命令":
                    self.meas_que.put(message)

    # 終了処理
    def end_loop(self):
        self.loop_flg = False

def main():
    # 初期化
    pygame.init()
    serial_op_que = queue.Queue()
    op_serial_que = queue.Queue()
    meas_que      = queue.Queue()
    # 通信用クラス生成 
    serial     = SerialUIBridge(SERIAL_PARAMS_GUI)
    do_serial  = SerialRead(serial,op_serial_que, serial_op_que, meas_que)
    # 寸法測定用
    indicator = DegitalIndicator(meas_que, serial)
    screen = pygame.display.set_mode((1920,1080))
    app    = Application(screen, serial,op_serial_que,serial_op_que)

    serial_thread = threading.Thread(target=do_serial.read)
    indicator_thread = threading.Thread(target=indicator.chack)
    serial_thread.start()
    indicator_thread.start()
    app.ran()
    
    do_serial.end_loop()
    indicator.end()
    serial_thread.join()
    indicator_thread.join()
    pygame.quit()

main()