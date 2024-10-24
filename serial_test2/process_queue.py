# queue_manager.py
from multiprocessing import Manager

class queue:
    def __init__(self):
        self.manager = Manager()
        self.send_queue = self.manager.Queue()
        self.receive_queue = self.manager.Queue()
        self.degital_queue = self.manager.Queue()
        self.user_queue = self.manager.Queue()        
    
    def get_queue(self):
        return self.send_queue, self.receive_queue, self.degital_queue, self.user_queue
        


