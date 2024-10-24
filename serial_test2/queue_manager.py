import struct
from queue import Queue

class QueueManager:
    def __init__(self, queues):
        self.send_queue = queues['send_queue']
        self.receive_queue = queues['receive_queue']

    def get_from_queue(self, queue):
        if not queue.empty():
            return queue.get()
        return None

    def put_in_queue(self, queue, word):
        if word is not None:
            queue.put(word)

    def send_queue_item(self):
        word = self.get_from_queue(self.send_queue)
        if word is None:
            return None        
        return self.to_byte(word)

    def to_byte(self, word):
        if isinstance(word, str):
            return word.encode('utf-8') if not word.isdigit() else self.int_to_byte(int(word))
        elif isinstance(word, int):
            return struct.pack('>B', word)
        elif isinstance(word, bytes):
            return word
        else:
            print("Invalid data type")
            return None

    def int_to_byte(self, word):
        return struct.pack('>B', word)
