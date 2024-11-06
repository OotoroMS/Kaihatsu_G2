#   データベース処理クラス-メイン装置
import sqlite3
import datetime
#   テーブル接続用クエリ
DB_CONNECT = "D:\\GitHub\\Kaihatsu_G2\\UI試作_Re\\GUI_option_test\\DB\\"
#   確認用クエリ
DB_LIST = "select * from "   #   データベース一覧を取得
TABLE_LIST = "show tables"      #   テーブル一覧を取得
TABLE_DATA_LIST = "select * from "  #   テーブルの中身取得

#   良否判定テーブル
GOOD_SIZE_UPDATE = "update DB_now set good_size = "
BAD_SIZE_UPDATE = "update DB_now set bad_size = "
GOOD_VISION_UPDATE = "update DB_now set good_vision = "
BAD_VISION_UPDATE = "update DB_now set bad_vision = "
#   不良品テーブル
TIMELOG_UPDATE = "insert into DB_timelog(datetime) values "

#   データベース通信用クラス
class SQLCommunication:
    #   コンストラクタ
    def __init__(self):
        self.db_name = ""
        self.table_name = ""
    
    #   データベース名を設定
    def set_db_name(self, database_name):
        self.db_name = database_name
    
    #   テーブル名を設定
    def set_table_name(self, set_table):
        self.table_name = set_table
    
    #   データベース表示
    def db_list_display(self,db_name=None):
        if db_name == None:
            db_name = self.db_name
        #   データベース接続
        con = sqlite3.connect(DB_CONNECT+db_name)
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
    def table_list_display(self, db_name=None):
        if db_name == None:
            db_name = self.db_name
         #   データベース接続
        con = sqlite3.connect(DB_CONNECT+db_name)
        #   カーソルを取得
        cursor = con.cursor()
        try:
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
    def table_data_list_display(self, db_name=None, table_name=None):
        #   データベース名の引数がなければ
        if db_name == None:
            db_name = self.db_name
        #   テーブル名の引数がなければ
        if table_name == None:
            table_name = self.table_name
        #   テーブル接続
        con = sqlite3.connect(DB_CONNECT+db_name)
        #   カーソルを取得
        cursor = con.cursor()
        try:
            #   テーブルからデータを取得するSQL文を生成
            que = TABLE_DATA_LIST + table_name
            #   テーブルを取得
            cursor.execute(que)
            #   結果を取り出す
            result = cursor.fetchall()
            for i in result:
                print(i)
        except Exception as e:
            print("DbCommunication:table_list_display error: ",e)
        finally:
            cursor.close()
            con.close()
    
    #   sql実行(戻り値なし 例:'insert', 'update'など)
    def db_query_execution(self,db_name=None,query=None):
        #   各種代入処理
        if db_name == None:
            db_name = self.db_name
        result = None
        #   クエリのみ代入なしの場合実行しない
        if query == None:
            print("Please specify the query to be executed as an argument.")
        else:
            #   テーブル接続
            con = sqlite3.connect(DB_CONNECT+db_name)
            try:
                #   カーソルを取得
                cursor = con.cursor()
                #   指定されたクエリを実行
                cursor.execute(query)
                result = cursor.fetchall()
                #   結果を適応
                con.commit()
            except Exception as e:
                print("DbCommunication:table_list_display error: ",e)
            finally:
                cursor.close()
                con.close()
            return result

    #   sql実行(戻り値あり 'select'など)
    def table_data_get(self, db_name=None,query=None):
        #   各種代入処理
        if db_name == None:
            db_name = self.db_name
        result = None
        #   クエリのみ代入なしの場合実行しない
        if query == None:
            print("Please specify the query to be executed as an argument.")
        else:
            #   テーブル接続
            con = sqlite3.connect(DB_CONNECT+db_name)
            try:
                #   カーソルを取得
                cursor = con.cursor()
                #   指定されたクエリを実行
                cursor.execute(query)
                #   テーブルのデータを取得
                result = cursor.fetchall()
            except Exception as e:
                print("DbCommunication:table_list_display error: ",e)
            finally:
                cursor.close()
                con.close()
            return result

    def  check_day(self,db_name=None):#db_nowの日付確認
        #   各種代入処理
        if db_name == None:
            db_name = self.db_name
        print("connect DB: ", db_name)
        con = sqlite3.connect(DB_CONNECT+db_name)
        day = datetime.datetime.today()
        today = day.date()
        try:
            #   カーソルを取得
            cursor = con.cursor()
            cursor.execute("select * from DB_now")
            result = cursor.fetchall()
            for i in result:
                db_day = i[1]
            if str(today) != str(db_day):
                cursor.execute("insert into DB_countlog(day,good_size,bad_size)values('%s',%d,%d)" %(i[1],i[2],i[3]))
                cursor.execute("update DB_now set day='%s',good_size=0,bad_size=0 where id=0" %(today))
                con.commit()
        except Exception as e:
                print("DbCommunication:check_day error: ",e)
        finally:
            cursor.close()
            con.close()


    def good_size_update(self, db_name=None):
        #   各種代入処理
        if db_name == None:
            db_name = self.db_name
        self.check_day(db_name)
        #   テーブル接続
        con = sqlite3.connect(DB_CONNECT+db_name)
        try:
            #   カーソルを取得
            cursor = con.cursor()
            cursor.execute("select * from DB_now")
            result = cursor.fetchall()
            for i in result:
                num01=i[2] + 1
            cursor.execute(GOOD_SIZE_UPDATE + str(num01) + " where id='0'")
            con.commit()
        except Exception as e:
                print("DbCommunication:good_size_update error: ",e)
        finally:
            cursor.close()
            con.close()
    
    def bad_size_update(self, db_name=None):
        #   各種代入処理
        if db_name == None:
            db_name = self.db_name
        #   テーブル接続
        self.check_day(db_name)
        con = sqlite3.connect(DB_CONNECT+db_name)
        try:
            #   カーソルを取得
            cursor = con.cursor()
            cursor.execute("select * from DB_now")
            result = cursor.fetchall()
            for i in result:
                num01=i[3] + 1
            cursor.execute(BAD_SIZE_UPDATE + str(num01) + " where id='0'")
            con.commit()
        except Exception as e:
                print("DbCommunication:bad_size_update error: ",e)
        finally:
            cursor.close()
            con.close()

    def good_vision_update(self, db_name=None):
        #   各種代入処理
        if db_name == None:
            db_name = self.db_name
        #   テーブル接続
        self.check_day(db_name)
        con = sqlite3.connect(DB_CONNECT+db_name)
        try:
            #   カーソルを取得
            cursor = con.cursor()
            cursor.execute("select * from DB_now")
            result = cursor.fetchall()
            for i in result:
                num01=i[2] + 1
            cursor.execute(GOOD_VISION_UPDATE + str(num01) + " where id='0'")
            con.commit()

        except Exception as e:
                print("DbCommunication:good_vision_update error: ",e)
        finally:
            cursor.close()
            con.close()

    def bad_vision_update(self, db_name=None):
        #   各種代入処理
        if db_name == None:
            db_name = self.db_name
        #   テーブル接続
        self.check_day(db_name)
        con = sqlite3.connect(DB_CONNECT+db_name)
        try:
            #   カーソルを取得
            cursor = con.cursor()
            cursor.execute("select * from DB_now")
            result = cursor.fetchall()
            for i in result:
                num01=i[3] + 1
            cursor.execute(BAD_VISION_UPDATE + str(num01) + " where id='0'")
            con.commit()
        except Exception as e:
                print("DbCommunication:bad_vision_update error: ",e)
        finally:
            cursor.close()
            con.close()
    
    def bad_time_update(self, db_name=None):
        #   各種代入処理
        if db_name == None:
            db_name = self.db_name
        con = sqlite3.connect(DB_CONNECT+db_name)
        try:
            #   カーソルを取得
            cursor = con.cursor()
            days = datetime.datetime.now().replace(microsecond=0)
            que = TIMELOG_UPDATE + "('" + str(days) + "')"
            print(que)
            cursor.execute(que)
            con.commit()
        except Exception as e:
                print("DbCommunication:bad_time_update error: ",e)
        finally:
            cursor.close()
            con.close()

if __name__ == "__main__":
    db = SQLCommunication()
    db.set_db_name("testdb_main.db")
    #db.set_table_name("db_now")
    #db.table_data_list_display(None,"db_countlog")#引数二つ必要なことに注意
    #db.db_query_execution(None,"")
    db.good_size_update()
    db.bad_size_update()
    db.table_data_list_display(table_name="DB_now")
    db.bad_time_update()