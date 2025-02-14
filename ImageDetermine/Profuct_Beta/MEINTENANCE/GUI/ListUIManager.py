import pygame
import queue
import threading
# 定数(各種コマンド)
from MEINTENANCE.CONSTANTS.pless_command    import *
from MEINTENANCE.CONSTANTS.command_type     import *
from MEINTENANCE.CONSTANTS.serial_result    import *
import MEINTENANCE.CONSTANTS.move_moter_pos as MOVE_MOTOR_POS
# 定数(GUI)
from MEINTENANCE.GUI.constants.UIManager_constant   import *
from MEINTENANCE.GUI.constants.screen_name          import *
from MEINTENANCE.GUI.constants.popup_name           import *
# マネージャー
from MEINTENANCE.GUI.managers.OperatingManager  import OperatingManager
from MEINTENANCE.GUI.managers.ScreenManager     import ScreenManager
from MEINTENANCE.GUI.managers.PopupManager      import PopupManager
from MEINTENANCE.QUEUE.QueueManager_list        import QueueManager

class UIMabager:
    def __init__(self, plc_cmd_que_list : list, plc_cmd_thred_lock : list, work_cmd_que_list : list, work_cmd_thred_lock: list, operation_que_list : list, operation_thread_lock : list) -> None:
        self.screen = pygame.display.set_mode(SCREEN_SIZE, pygame.FULLSCREEN)
        # 各マネージャー
        self.operation_manager  = OperatingManager(self.screen)
        self.screen_manager     = ScreenManager(self.screen)
        self.popup_manager      = PopupManager(self.screen)
        self.queue_manager      = QueueManager(plc_cmd_que_list, plc_cmd_thred_lock, work_cmd_que_list, work_cmd_thred_lock, operation_que_list, operation_thread_lock)
        # 現在の画面
        self.curent_screen = MAIN
        self.running = True
        # 押しっぱなしフラグ
        self.is_hold_down = False
        self.hold_down_command = None
        # 更新頻度設定用
        self.clock = pygame.time.Clock()
        # 稼働状況保持用
        self.operation_status = ["停止中", "プログラムに問題があります"]
        self.work_status = [b'\xcd', b'\xd0']
        self.move_log = None
    
    def run(self):
        while self.running:
            self.get_opration_stutus()
            self.get_work_status()
            self.screen_manager.work_lamp_update(self.work_status)
            draw_result = self.screen_manager.screen_draw(self.curent_screen)
            self.operation_manager.status_receve_draw(self.operation_status)
            if draw_result:
                self.check_event()
            # 画面更新   
            pygame.display.update()
            self.clock.tick(FPS)

    # イベントを判別
    def check_event(self):
        event_result, is_click = self.screen_manager.screen_event_check(self.curent_screen)
        screen_result = self.screen_event(event_result, is_click)
        if not screen_result:
            self.button_backend_event(event_result, is_click)

    # 画面表示イベント
    def screen_event(self, event_result, is_click):
        if is_click and self.screen_manager.screen_search(event_result):
            self.curent_screen = event_result
            return True
        if is_click and self.popup_manager.popup_search(event_result):
            self.show_popup(event_result)
            return True
        return False

    # ポップアップ表示
    def show_popup(self, popup_name):
        while True:
            self.popup_manager.popup_draw(popup_name)
            result, action = self.popup_manager.popup_event_check(popup_name)
            if result == DB_RESET:
                self.db_reset()
                break
            elif result == END:
                self.queue_manager.send_plc_command(APP_END)
                self.queue_manager.recv_plc_command()
                self.running = False
                break
            elif action:
                break
            pygame.display.update()

    # バックエンド関連のイベント(こちらから送る処理)
    def button_backend_event(self, event_result, is_click):
        if is_click and event_result in PUSH_COMMAND.keys():        # 押したときのイベントなら
            self.push_command_event(event_result)
        elif is_click and self.curent_screen == CHANGE:             # パスワード更新のイベントなら
            self.password_update(event_result)
        elif is_click and event_result in ADSORPTION_COMMAND.keys():
            self.adsorption_event(event_result)
        elif is_click and event_result in LIGHT_COMMAND.keys():
            self.light_event(event_result)
        elif is_click and event_result in HOLD_DOWN_COMMAND.keys(): # 押しっぱなしの開始イベントなら
            self.hold_down_start(event_result)
        elif is_click and event_result == HOLD_DOWN_END:            # ボタンを離したときのイベントなら
            # print("UIManager.py button_backend_event : Hold down end.")
            self.hold_down_end(event_result)
        elif self.is_hold_down:                                     # 押しっぱなしの処理が有効なら
            # print("UIManager.py button_backend_event : Hold down.")
            self.hold_down()

    # ボタン押下時の処理
    def push_command_event(self, key : str):
        # 押されたボタン識別子を渡す
        self.queue_manager.send_two_message(PLC, key)
        self.lamp_update(key, RUN)
        # 受信するまで待機
        result = self.queue_manager.recv_plc_command()
        if result:
            print("UIManager.py push_command_event : result is ", result)
        if len(result) == 2 and result[0] == NORMAL:
            self.lamp_update(key, FINISH)

    # パスワード更新
    def password_update(self, result : str):
        if result and result[:6] == UPDATE_PASS:
            new_password = result[6:]
            self.queue_manager.send_two_message(PASSWORD, new_password)
            result = self.queue_manager.recv_plc_command()
            if result == SUCCESS:
                # パスワード更新のPOPUP表示
                self.show_popup(CHANGE_POPUP)
                self.curent_screen = MAIN

    # 吸着ボタンの処理
    def adsorption_event(self, key : str):
        self.queue_manager.send_two_message(ADSORPTION, key)
        result = self.queue_manager.recv_plc_command()
        if result == SUCCESS:
            print("UIManager.py adsorption_event : update")

    def light_event(self, key : str):
        self.queue_manager.send_two_message(LIGHT, key)
        print("UIManager.py light_event : send")
        result = self.queue_manager.recv_plc_command()
        if result == SUCCESS:
            print("UIManager.py light_event : update")

    # ボタンのホールド処理(開始)
    def hold_down_start(self, key : str):
        # print("UIManager.py hold_down_start : Hold down start.")
        self.queue_manager.send_two_message(HOLD_DOWN_START, key)
        result = self.queue_manager.recv_plc_command()
        if result == SUCCESS:
            self.lamp_update(key, RUN)
            self.is_hold_down = True
            self.hold_down_command = key
            # if self.move_log:
            #     self.lamp_update(self.hold_down_command, self.move_log)
            # テスト
            # self.queue_manager.send_plc_command(HOLD_DOWN)
            # result = self.queue_manager.recv_plc_command()

    # ボタンのホールド処理(継続)
    def hold_down(self):
        self.queue_manager.send_plc_command(HOLD_DOWN)
        result = self.queue_manager.hold_mode_recv_message()
        if result:
            print("UIManager.py hold_down : result is ", result)
            self.lamp_update(self.hold_down_command, result)
            print
            # print("UIManager.py hold_down : update")

    # ボタンのホールド処理(終了)
    def hold_down_end(self, key : str):
        self.hold_down()
        self.is_hold_down = False
        self.queue_manager.send_plc_command(key)
        while True:
            result = self.queue_manager.recv_plc_command()
            # print(result)
            if result == SUCCESS:
                break
        # print("UIManager.py hold_down_end : Hold down end.")

    # データベース初期化
    def db_reset(self):
        self.queue_manager.send_message(DB_RESET)
        result = self.queue_manager.until_recv_message()
        if result == SUCCESS:
            while True:
                self.popup_manager.popup_draw(SUCCESS_POPUP)
                result, action = self.popup_manager.popup_event_check(SUCCESS_POPUP)
                if action:
                    break
                pygame.display.update()

    def lamp_update(self, key : str, opration : str):
        # 押しっぱなし処理なら
        if key in HOLD_DOWN_COMMAND.keys():
            self.screen_manager.move_lamp_update(opration, key)
        # 押したときの処理なら
        elif key in PUSH_COMMAND.keys():
            if opration == RUN:
                self.screen_manager.screen_lamp_update_yellow(key)
            elif opration == FINISH:
                self.screen_manager.screen_lamp_update_green(key)
        pygame.display.update()

    # 稼働状況を取得し描画
    def get_opration_stutus(self):
        self.queue_manager.send_plc_command(OPERATION_STATUS)
        # result = self.queue_manager.recv_operation_command()
        # if result:
        #     self.operation_status = result
            # print("UIManager.py get_opration_status :",result)
    
    # ワーク検知
    def get_work_status(self):
        self.queue_manager.send_plc_command(WORK_STATUS)
        result = self.queue_manager.recv_work_command()
        if result:
            self.work_status = result

            # print("UIManager.py get_work_status :",result)
    # なくなるまで取り出す
    def plc_que_data_get_all(self):
        while True:
            result = self.queue_manager.hold_mode_recv_message()
            # print("UIManager.py plc_que_data_get_all : result is ", result)
            if result in MOVE_MOTOR_POS.MOTOR_POS_LIST:
                self.move_log = result
                # print("UIManager.py plc_que_data_get_all : move_log is ", self.move_log)
            else:
                return result
            
    
