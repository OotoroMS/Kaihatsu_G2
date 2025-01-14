# 統括プログラムの予定
import pygame
import serial
import threading
# 自作モジュール
from GUI.application                import Application
from SERIAL.manager.SerialUIBridge  import SerialUIBridge
from DEGITALINDICATOR.Meas          import MeasurementConverter

PORT1 = "COM3" # 適切なポートに変更してください
BAUD_RATE = 9600
TIMEOUT = 0.08
PARITY = serial.PARITY_EVEN
STOPBITS = serial.STOPBITS_ONE

SERIAL_PARAMS_GUI = {
    "port": PORT1,
    "baudrate": BAUD_RATE,
    "parity": PARITY,
    "stopbits": STOPBITS,
    "timeout": TIMEOUT
}
SERIAL_PARAMS_DE  = {
    "port"      : None,
    "baudrate"  : 2400,
    "parity"    : serial.PARITY_NONE,
    "stopbits"  : serial.STOPBITS_ONE,
    "timeout"   : 0.08
}
class SerialRead:
    def __init__(self, serial : SerialUIBridge):
        self.serial   = serial
        self.loop_flg = True
    
    def read(self):
        while self.loop_flg:
            self.serial.read_loop()

    def end_loop(self):
        self.loop_flg = False

def main():
    # 初期化
    pygame.init()

    # 通信用クラス生成
    serial     = SerialUIBridge(SERIAL_PARAMS_GUI)
    do_serial  = SerialRead(serial)
    # インジケータ
    de = MeasurementConverter()

    screen = pygame.display.set_mode((1920,1080))
    app    = Application(screen, serial)

    serial_thread = threading.Thread(target=do_serial.read)
    serial_thread.start()
    app.ran()
    
    do_serial.end_loop()
    serial_thread.join()
    pygame.quit()

main()