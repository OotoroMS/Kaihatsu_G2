#   送信と受信ができるか確認するプログラム
import serial
import time

#   データ受信関数
def get_data(ser:serial):
    rcv_data = ser.read(13)
    return rcv_data

#   メイン関数
def main():
    data_snd_msg = '1'
    data_rcv_msg = ""
    print("serial test start!!")
    #   1回目
    print("1st")
    #   シリアル通信開始
    ser=serial.Serial("COM8", baudrate=2400,parity=serial.PARITY_NONE,bytesize=serial.EIGHTBITS,stopbits=serial.STOPBITS_ONE,timeout=5)
    #   3秒待つ
    time.sleep(3)
    try:
        #   要求信号送信
        ser.write(data_snd_msg.encode())
        #   測定データ受信
        data_rcv_msg = get_data(ser)
        #   もしデータがなければ
        if data_rcv_msg == b'':
            print('no data')
        else:
            #   データを表示
            print(data_rcv_msg)
        pass
    #   エラー発生時
    except Exception as e:
        print("エラー\n")
        print(e)
    #   シリアル通信終了
    ser.close()
    #   2回目
    print('2nd')
    ser=serial.Serial("COM8", baudrate=2400,parity=serial.PARITY_NONE,bytesize=serial.EIGHTBITS,stopbits=serial.STOPBITS_ONE,timeout=5)
    try:
        #   要求信号送信
        ser.write(data_snd_msg.encode())
        #   測定データ受信
        data_rcv_msg = get_data(ser)
        #   もしデータがなければ
        if data_rcv_msg == b'':
            print('no data')
        else:
            #   データを表示
            print(data_rcv_msg)
        pass
    #   エラー発生時
    except Exception as e:
        print("エラー\n")
        print(e)
    #   シリアル通信終了
    ser.close()
    print("test end...")

if __name__ == "__main__":
    main()