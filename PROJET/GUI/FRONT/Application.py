# GUI/FRONT/Application.py

# デバック用
import sys
import os
sys.path.append(os.getcwd())

import importlib
from queue import Queue
import pygame

# 自作プログラムをimport
from GUI.FRONT.screen.BaseScreen import BaseScreen
# 定数ファイル
from GUI.FRONT.constant.screen_list import screen_names

class Application:
    def __init__(self, screen: pygame.Surface, to_back: Queue, from_back: Queue):
        self.screen: pygame.Surface = screen
        self.current_screen: BaseScreen = None
        self.screens: dict = {}  # 全ての画面インスタンスを保持する辞書
        self.screen_names = screen_names  # 外部ファイルから画面リストを取得
        self.to_back = to_back  # フロントからバックへのキュー
        self.from_back = from_back  # バックからフロントへのキュー
        self.initialize_screens()  # 全画面を最初に作成

    # 画面の作成+辞書に追加
    def initialize_screens(self):
        for screen_name in self.screen_names:
            if screen_name not in self.screens:
                try:
                    module = importlib.import_module(f"GUI.FRONT.screen.{screen_name}")
                    screen_class = getattr(module, screen_name)  # クラスを取得
                    # 画面クラスをインスタンス化して辞書に格納
                    self.screens[screen_name] = screen_class(self.screen, self.to_back)
                except (ModuleNotFoundError, AttributeError) as e:
                    print(f"Error: Failed to load screen '{screen_name}'. {e}")

    # 画面の切替
    def change_screen(self, screen_name: str):
        if screen_name in self.screens:
            self.current_screen = self.screens[screen_name]
        else:
            print(f"Error: Screen '{screen_name}' not found.")

    # バックからの応答を処理
    def handle_back_response(self):
        # バックからの応答を受け取る
        if not self.from_back.empty():
            response = self.from_back.get()
            print(f"バックからのレスポンス: {response}")
            if response in self.screens:  # レスポンスが辞書のキーとして存在すればその画面に遷移
                self.change_screen(response)  # レスポンスに基づいて画面遷移を行う

    # メインループ
    def run(self):
        is_run = True
        self.change_screen("BaseScreen")  # 初期画面を設定
        while is_run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    is_run = False
                elif self.current_screen:
                    self.current_screen.handle_event(event)  # 現在の画面のイベント処理
            
            # 現在の画面の描画
            if self.current_screen:
                self.current_screen.draw()

            # バックからの応答を処理
            self.handle_back_response()
            
            pygame.display.update()


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((1920, 1080))
    app = Application(screen)   # クラスをインスタンス化
    app.run()
    pygame.quit()
