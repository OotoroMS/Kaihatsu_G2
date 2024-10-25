from multiprocessing import Queue, Manager
from typing import Dict

class QueueCreate:
    def __init__(self):
        """
        初期化メソッド。用途ごとに異なるキューを作成し、`communication_queues` と `data_processing_queues` 
        の辞書に格納する。
        """
        self.manager = Manager()
        # 通信に使用するキューの辞書
        self.communication_queues: Dict[str, Queue] = {
            'send_queue': self.manager.Queue(),
            'receive_queue': self.manager.Queue(),
        }
        # データ処理に使用するキューの辞書
        self.data_processing_queues: Dict[str, Queue] = {
            'digital_queue': self.manager.Queue(),
            'user_queue': self.manager.Queue(),
        }

    def get_communication_queues(self) -> Dict[str, Queue]:        
        """
        通信用キューを格納した辞書を返す。

        戻り値:
            Dict[str, Queue]: 通信用キュー (`send_queue` と `receive_queue`) の辞書
        """
        return self.communication_queues

    def get_data_processing_queues(self) -> Dict[str, Queue]:        
        """
        データ処理用キューを格納した辞書を返す。

        戻り値:
            Dict[str, Queue]: データ処理用キュー (`digital_queue` と `user_queue`) の辞書
        """
        return self.data_processing_queues
