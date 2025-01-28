import pygame
import serial
import MEINTENANCE.Maintenance
import MAIN_OPRATION.MainOpration
MAIN      = "main"
OPERATION = "operation"

SERIAL_PARAMS_GUI = {
    "port": "COM3",
    "baudrate": 9600,
    "parity": serial.PARITY_NONE,
    "stopbits": serial.STOPBITS_ONE,
    "timeout": 0.1
}

def main():
    mode = MAIN
    loop = True
    while loop:
        if mode == MAIN:
            result = MAIN_OPRATION.MainOpration.MainOpration(SERIAL_PARAMS_GUI)
            if result == OPERATION:
                mode = OPERATION
            elif result == "end":
                loop = False
        elif mode == OPERATION:
            # メンテナンス動作
            MEINTENANCE.Maintenance.Maintenance(SERIAL_PARAMS_GUI)
            mode = MAIN

if __name__ == "__main__":
    pygame.init()
    main()
    pygame.quit()