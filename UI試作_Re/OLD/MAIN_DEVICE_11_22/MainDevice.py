# 統括プログラムの予定
import pygame
import serial
# 自作モジュール
from GUI.application   import Application
from SERIAL.plc_pc     import SerialManager
from SERIAL.pc_comands import PCManager
PORT1 = "COM4"  # 適切なポートに変更してください
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

def main():
    # 初期化
    pygame.init()

    # 通信用クラス生成
    serial     = SerialManager(SERIAL_PARAMS_GUI)
    pc_manager = PCManager(serial)
    screen = pygame.display.set_mode((1920,1080))
    app    = Application(screen, pc_manager)

    app.ran()
    pygame.quit()

main()