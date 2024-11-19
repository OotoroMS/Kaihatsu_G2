from comunication.plc_pc import SerialManager
from comunication.pc_comands import PCManager
import pygame
import App
import serial

FONT = "C:\\Windows\\Fonts\\msgothic.ttc"

# シリアルポートの設定
PORT1 = "COM8"  # 適切なポートに変更してください
BAUD_RATE = 9600
TIMEOUT = 0.08
PARITY = serial.PARITY_EVEN
STOPBITS = serial.STOPBITS_ONE


if __name__ == "__main__":
    pygame.init()
    # 試験用
    serial_params1 = {
    "port": PORT1,
    "baudrate": BAUD_RATE,
    "parity": PARITY,
    "stopbits": STOPBITS,
    "timeout": TIMEOUT,
    }
    serial_comm1 = SerialManager(serial_params1)
    serial_test  = PCManager(serial_comm1)    
    screen       = pygame.display.set_mode((1920,1080))
    app          = App.App(screen,FONT,serial_test)
    app.run()
    pygame.quit()