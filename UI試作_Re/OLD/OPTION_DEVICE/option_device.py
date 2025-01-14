import pygame
import serial
import GUI.application
from SERIAL.plc_pc     import SerialManager
from SERIAL.pc_comands import PCManager

PORT1 = "COM8"  # 適切なポートに変更してください
BAUD_RATE = 9600
TIMEOUT   = 0.08
PARITY    = serial.PARITY_EVEN
STOPBITS  = serial.STOPBITS_ONE

SERIAL_PARAMS_GUI = {
    "port": PORT1,
    "baudrate": BAUD_RATE,
    "parity": PARITY,
    "stopbits": STOPBITS,
    "timeout": TIMEOUT
}

pygame.init()
serial     = SerialManager(SERIAL_PARAMS_GUI)
pc_manager = PCManager(serial)
screen = pygame.display.set_mode((1920,1080))
app = GUI.application.Application(screen, pc_manager)
app.run()
pygame.quit()
