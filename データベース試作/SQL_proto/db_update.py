import random
import time
import datetime

import SQLCommunication_main as SQc
import Measurement as Meas

DB_NAME = "testdb_option.db"

#   ダミーデータ生成
def data_rand():
    rand = random.randint(0,15)
    sign = random.randint(0,10)
    if sign < 5:
        if rand < 10:
            damy_str = '01A-00000.0%d\r' % (rand)
        else:
            damy_str = '01A-00000.%d\r' % (rand)
            damy_ary = bytearray(damy_str.encode())
            damy = bytes(damy_ary)
            print("str :",damy_str)
            print("bytearray ;",damy_ary)
            print("bytes :", damy)
    else:
        if rand < 10:
            damy_str = '01A+00000.0%d\r' % (rand)
        else:
            damy_str = '01A+00000.%d\r' % (rand)
    
    damy_ary = bytearray(damy_str.encode())
    damy = bytes(damy_ary)

    return damy

#   結果変換・保存
def meas_change(byte : bytes):
    meas = Meas.Measurement()
    db = SQc.SQLCommunication()
    db.set_db_name(DB_NAME)#"testdb_02" DB_NAME
    float_result = meas.chenge_byte_float(byte)
    que = "insert into DB_sizelog(datetime,sizelog) values (datetime('now'), {:.2f})".format(float_result)
    db.db_query_execution(query=que)
    return float_result

#   良否判定・保存
def meas_judgment(val : float):
    meas = Meas.Measurement()
    db = SQc.SQLCommunication()
    db.set_db_name(DB_NAME)#"testdb_02.db" DB_NAME
    judgment_result = meas.judgment_size(val)
    if judgment_result:
        db.good_size_update()
    else:
        db.bad_size_update()
        db.bad_time_update()
    print("判定結果 ")
    db.table_data_list_display(db_name=DB_NAME,table_name="DB_now")
    print("発生時刻 ")
    db.table_data_list_display(db_name=DB_NAME,table_name="DB_timelog")

if __name__ == "__main__":
    byte = data_rand()
    day = datetime.datetime.now().replace(microsecond=0)
    float_val = meas_change(byte)
    print("測定値 :",float_val)
    meas_judgment(float_val)
    

