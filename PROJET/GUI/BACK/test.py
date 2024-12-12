# GUI/BACK/test.py

from queue import Queue
import time

def background_task(to_back: Queue, from_back: Queue):
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
        time.sleep(0.01)    # CPU使用率の低下
