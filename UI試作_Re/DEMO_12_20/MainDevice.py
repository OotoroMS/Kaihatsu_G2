# 統括プログラムの予定
import pygame
import serial
import threading
# 自作モジュール
from GUI.application        import Application
from SERIAL.plc_pc          import SerialManager
from SERIAL.do_serial       import DoSerial
from DEGITALINDICATOR.Meas  import Meas

PORT1 = None  # 適切なポートに変更してください
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

def main():
    # 初期化
    pygame.init()

    # 通信用クラス生成
    serial     = SerialManager(SERIAL_PARAMS_GUI)
    do_serial = DoSerial(serial)
    # インジケータ
    de = Meas(SERIAL_PARAMS_DE)

    screen = pygame.display.set_mode((1920,1080))
    app    = Application(screen, do_serial)

    serial_thread = threading.Thread(target=do_serial.receive_loop)
    serial_thread.start()
    app.ran()
    
    do_serial.colse()
    serial_thread.join()
    pygame.quit()

main()