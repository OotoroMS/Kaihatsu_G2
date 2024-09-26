import random
import time
import DbCommunication as DbCom
import Measurement as Meas

def main():
    #   初期宣言
    db = DbCom.DbCommunication()    #   データベース
    damy = b''  #   測定値(ﾀﾞﾐｰﾃﾞｰﾀ)
    for i in range(0,10,1):
        rand = random.randint(0,12)
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
        # print("str :",damy_str)
        # print("bytearray ;",damy_ary)
        # print("bytes :", damy)
        meas = Meas.Measurement()
        float_result = meas.chenge_byte_float(damy)
        print("float_result :", float_result)
        que = "insert into DB_sizelog(datetime,sizelog) values (now(), {:.2f})".format(float_result)
        print("que :", que)
        db.db_query_execution(db_name="testdb_02", query=que)
        print("データベースのデータチェック")
        time.sleep(1)
    db.table_data_list_display(db_name="testdb_02",table_name="DB_sizelog")

if __name__ == "__main__":
    main()
