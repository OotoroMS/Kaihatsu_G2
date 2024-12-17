# GUI/BACK/test.py

from queue import Queue
import time
from SERIAL.manager.serial_communicator import SerialCommunicator
from SERIAL.manager.plc_base_handler    import PLCBaseHandler
from SERIAL.constant.Status             import OperationStatus

def background_task(to_back: Queue, from_back: Queue, serial: PLCBaseHandler):
    while True:
        # フロントからの要求を待つ
        if not to_back.empty():
            message = to_back.get()
            if message == "MainScreen":
                # 画面変更の命令をフロントに返す
                from_back.put("MainScreen")  # 次に表示する画面名
            if message == "BaseScreen":
                # 画面変更の命令をフロントに返す
                from_back.put("BaseScreen")
            if message == "NG":
                from_back.put("NG")
            if message == "End":
                from_back.put("End")
            if message == "EndPopup":
                from_back.put("EndPopup")
            if message == "OriginReset":
                # ポップアップを消す
                from_back.put("NG")
                # 特定のコマンドを送信
                bytes_data = serial.format_int(17)
                serial.send(bytes_data)
            if message == "OriginNotReset":
                from_back.put("NG")
                # 特定のコマンドを送信
                bytes_data = serial.format_int(19)
                serial.send(bytes_data)
        # シリアル通信の受信を受け取る        
        data, status = serial.read()
        if status == OperationStatus.SUCCESS:
            print(data)
            number = int.from_bytes(data, byteorder='big')
            print(number)
            if number == 15:
                from_back.put("OriginResetPopup")
            elif number == 42:
                # デジタルインジケータを実行
                measure = 7.56
                result = "OK"                
                # 結果によって異なるデータを送信+ポップアップを表示
                from_back.put(["MeasurePopup", f"測定値:{measure}mm\n 判定結果:{result}"])
                # OK = 44 NG = 46
                if result == "OK":
                    bytes_data = serial.format_int(44)
                    serial.send(bytes_data)
                elif result == "NG":
                    bytes_data = serial.format_int(46)
                    serial.send(bytes_data)
        time.sleep(0.01)    # CPU使用率の低下
