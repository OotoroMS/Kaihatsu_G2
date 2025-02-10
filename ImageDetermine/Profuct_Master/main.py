import pygame
import serial
import MEINTENANCE.Maintenance
import MAIN_OPRATION.MainOpration
import json

MAIN      = "main"
OPERATION = "operation"

SERIAL_PARAMS_GUI = {
    "port": "COM3",
    "baudrate": 9600,
    "parity": serial.PARITY_NONE,
    "stopbits": serial.STOPBITS_ONE,
    "timeout": 0.08
}

def main():
    mode = MAIN
    loop = True

    # シリアル通信の設定を読み込む
    serial_settings_path = "SERIAL/serial_settings.json"
    with open(serial_settings_path, "r") as f:
        j_data = json.load(f)
        SERIAL_PARAMS_GUI["port"] = j_data["port"]
        SERIAL_PARAMS_GUI["baudrate"] = j_data["baudrate"]
        SERIAL_PARAMS_GUI["timeout"] = j_data["timeout"]

    # メインループ
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