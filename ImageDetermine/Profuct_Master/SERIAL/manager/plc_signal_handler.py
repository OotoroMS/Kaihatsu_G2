# SERIAL/manager/do_serial.py

# 自作プログラムをimport
# 型チェックのデコレータ, エラー文表示
from UTILS.type_check import type_check_decorator
import UTILS.log_config as log_config
# PLCからの受信データを周辺機能にわかりやすい形で渡すクラス(このクラスの親)
from SERIAL.manager.plc_base_handler import PLCBaseHandler
# PLCとの通信処理に基づいた処理を行うクラス
from SERIAL.manager.plc_communicator import PLCCommunicator

# PLCとのやり取りを監視して、結果を各クラスに渡す
class PLCSignalHandler(PLCBaseHandler):
    def __init__(self, plc_communicator: PLCCommunicator):
        super().__init__(plc_communicator)
        # ループ管理用変数
        self.is_loop: bool = True

    # 受信ループ処理
    # この関数はスレッド化する予定
    def receive_loop(self):
        while self.is_loop:
            try:
                super().receive()
            except Exception as e:
                log_config(self, self.receive_loop.__name__, e)

    
    def close(self):
        self.is_loop = False
        super().close()

if __name__ == '__main__':
    pass
