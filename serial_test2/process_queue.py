from multiprocessing import Manager

class QueueCreate:
    def __init__(self):
        self.manager = Manager()
        # 用途ごとの辞書を作成
        self.communication_queues = {
            'send_queue': self.manager.Queue(),
            'receive_queue': self.manager.Queue(),
        }
        self.data_processing_queues = {
            'digital_queue': self.manager.Queue(),
            'user_queue': self.manager.Queue()
        }

    def get_communication_queues(self):        
        return self.communication_queues

    def get_data_processing_queues(self):        
        return self.data_processing_queues
