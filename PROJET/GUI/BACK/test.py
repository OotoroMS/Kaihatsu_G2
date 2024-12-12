# GUI/BACK/test.py

from queue import Queue
import time
from SERIAL.manager.serial_communicator import SerialCommunicator
from SERIAL.constant.Status             import OperationStatus

def background_task(to_back: Queue, from_back: Queue, serial: SerialCommunicator):
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
                from_back.put("NG")
        # シリアル通信の受信を受け取る
        data, status = serial.serial_read()
        if status == OperationStatus.SUCCESS:
            print(data)
            if data == b'23':
                from_back.put("OriginResetPopup")
            elif data == b'53':
                from_back.put(["MeasurePopup", "測定値: 10.3 mm"])
            elif data == b'54':
                from_back.put(["MeasurePopup", "測定値: 15.3 mm"])
        time.sleep(0.01)    # CPU使用率の低下
