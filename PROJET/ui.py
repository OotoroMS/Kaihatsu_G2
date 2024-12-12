# ui.py

import threading
from queue import Queue
import pygame

# Application と background_task のインポート
from GUI.FRONT.Application import Application
from GUI.BACK.test import background_task

def main():
    pygame.init()
    screen = pygame.display.set_mode((1920, 1080))

    # フロントとバックのキュー
    to_back = Queue()
    from_back = Queue()

    # Application のインスタンス化
    app = Application(screen, to_back, from_back)

    # スレッドでバックエンドの処理を開始
    backend_thread = threading.Thread(target=background_task, args=(to_back, from_back))
    backend_thread.daemon = True  # メインスレッドが終了するとバックグラウンドスレッドも終了
    backend_thread.start()

    # アプリケーションのメインループを実行
    app.run()

if __name__ == "__main__":
    main()
