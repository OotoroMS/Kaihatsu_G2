import serial
import threading
import time

# COM番号
PORT = "COM10"
                
# データ受信関数
def receive_data(serial_port):
    try:
        # シリアルポートの接続
        port = serial.Serial(serial_port,9600,timeout=0.1)   
        print(f"Serial Port connect:{port.name}")
        while True:
            if port.in_waiting > 0:                
                data = port.read(255).decode('utf-8')
                print(f'Received from {port.name}: {data}')
    except serial.SerialException as e:
        print("Cnnect Error")
    finally:
        port.close()  # 必ずポートをクローズする


if __name__ == "__main__":
    try:          
        # スレッドを作成して開始
        thread1 = threading.Thread(target=receive_data, args=(PORT,))
        thread1.start()
        while thread1.is_alive():
                thread1.join(timeout=0.1)
    except KeyboardInterrupt:
        print("中断")
    finally: 
        if thread1 and thread1.is_alive():
            thread1.join()              
        print("end")