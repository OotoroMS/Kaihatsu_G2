import threading            #   スレッド用モジュール
import time                 #   タイマーモジュール
import mysql.connector      #   データベース接続用モジュール

global TLOCK

#   DB接続用
HOST_NAME   = "172.21.23.51"
USER_NAME   = "testuser"
DB_PASSWORD = "is@55870129P"
#   接続命令
DB_CONNECT = "use "
#   SQL命令
DB_LIST    = "show databases"
TABLE_LIST = "show tables"

#   データベース通信用クラス
class DbCommunication:
    #   コンストラクタ
    def __init__(self):
        self.host = HOST_NAME
        self.user = USER_NAME
        self.password = DB_PASSWORD
        self.db_name = ""
        self.table_name = ""
    
    #   データベース名を設定
    def set_db_name(self, set_db_name):
        self.db_name = set_db_name
    
    #   テーブル名を設定
    def set_table_name(self, set_table_name):
        self.table_name = set_table_name
    
    #   データベース表示
    def db_list_display(self):
        #   データベース接続
        con = mysql.connector.connect(host = self.host, user = self.user, password = self.password)
        #   カーソルを取得
        cursor = con.cursor()
        try:
            #   データベース取得
            cursor.execute(DB_LIST)
            #   結果を取り出す
            result = cursor.fetchall()
            #   結果を表示
            print("データベース")
            for i in result:
                print(i)
        except Exception as e:
            print("DbCommunication:db_list_display error: ",e)
        finally:
            cursor.close()
            con.close()
    
    #   データベーステーブル表示
    def table_list_display(self, db_name=self.db_name):
         #   データベース接続
        con = mysql.connector.connect(host = self.host, user = self.user, password = self.password)
        #   カーソルを取得
        cursor = con.cursor()
        try:
            connect = DB_CONNECT + db_name
            #   データベース接続
            cursor.execute(connect)
            #   テーブルを取得
            cursor.execute(TABLE_LIST)
            #   結果を取り出す
            result = cursor.fetchall()
            for i in result:
                print(i)
        except Exception as e:
            print("DbCommunication:table_list_display error: ",e)
        finally:
            cursor.close()
            con.close()
    
    #   データベースの中身を表示
    def table_data_list_display(self, db_nmae, table_name):
        pass

        

#   メイン関数
def main():
    db = DbCommunication()
    print("test 1")
    db.db_list_display()
    print("TEST 2")
    db.table_list_display(db_name="testdb_02")
    print("test 3")
    db.set_db_name("testdb_02")
    db.table_list_display()
    print("end....")

if __name__ == "__main__":
    main()
