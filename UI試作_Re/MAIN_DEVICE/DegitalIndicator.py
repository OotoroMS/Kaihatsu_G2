import queue

from DEGITALINDICATOR.Indicator     import Indicator
from DATABASE.SQLCommunication      import SQLCommunication
from SERIAL.manager.SerialUIBridge  import SerialUIBridge
GET_VALUE = "SELECT calibrate_value FROM indicator"
SIZE_LOG  = "insert into DB_sizelog(datetime,sizelog) values (now(), {:.2f})"
VAITAL   = "データ取得"


class DegitalIndicator:
    def __init__(self, recv_que : queue.Queue, serial : SerialUIBridge) -> None:
        self.indicator = Indicator()
        self.db        = SQLCommunication()
        self.que       = recv_que
        self.serial    = serial
        self.loop_frg  = True
        self.db.set_db_name("testdb_main.db")

    def chack(self):
        message = None
        while self.loop_frg:
            # 稼働状況取得
            if not self.que.empty():
                message = self.que.get()
            # 稼働中の間だけデータを
            if message == VAITAL:
                db_data = self.db.db_query_execution(query=GET_VALUE)
                default_data = db_data[0][0]
                if default_data:
                    value, result = self.indicator.main(default_data)
                    if result == "OK":
                        self.db.good_size_update()
                        self.serial.send_set(["良品", "寸法部"])
                    elif result == "NG":
                        self.db.bad_size_update()
                        self.db.bad_time_update()
                        self.serial.send_set(["不良品", "寸法部"])
                    self.db.db_query_execution(query=SIZE_LOG.format(value))
    
    def end(self):
        self.loop_frg = False

if __name__ == "__main__":
    a = DegitalIndicator()
    a.chack()