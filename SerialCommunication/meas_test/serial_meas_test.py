import serial
import time
import sys

import Measurement as Meas

COM = "COM4"

#   シリアル通信プログラム(引数:通信先、送信データ 戻り値:測定値)
def get_data(ser : serial, snd_msg : str) -> bytes:
    #print("serial test start!!")
    try:
        ser.write(snd_msg.encode())     #   データ取得命令を送信
        rcv_msg = ser.read(13)          #   データを取得
    except Exception as e:              #   エラー発生時
        print("エラー\n")               #   画面にｴﾗｰの内容を表示   
        print(e)
    
    return rcv_msg

def main():
    # args = sys.argv
    # com = args[1]
    # ser = serial.Serial(com, baudrate=2400,parity=serial.PARITY_NONE,bytesize=serial.EIGHTBITS,stopbits=serial.STOPBITS_ONE,timeout=5)
    rcv_msg = ""    #   測定データ格納用
    meas = Meas.Measurement()
    ser = serial.Serial(COM, baudrate=2400,parity=serial.PARITY_NONE,bytesize=serial.EIGHTBITS,stopbits=serial.STOPBITS_ONE,timeout=5)
    time.sleep(3)
    try:
        print("g: get data q:exit")
        while 1:
            keyboard_input = input()
            if keyboard_input == "g":
                data_rcv_msg = get_data(ser, "s")
                #qprint(data_rcv_msg)
                meas_val = meas.chenge_byte_float(data_rcv_msg)
                meas_result = meas.judgment_size(meas_val)
                if meas_result:
                    print("測定値: ", meas_val, "判定結果: 良品")
                else:
                    print("測定値: ", meas_val, "判定結果: 不良品")
            elif keyboard_input == "q":
                print("end....")
                break
    except Exception as e:
        print("main erorr:", e)
    finally:
        ser.close()

if __name__ == "__main__":
    main()