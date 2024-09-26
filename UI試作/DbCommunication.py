#   データベース処理クラス
import mysql.connector      #   データベース接続用モジュール

#   DB接続用
HOST_NAME   = "172.21.23.51"
USER_NAME   = "testuser"
DB_PASSWORD = "is@55870129P"
#   テーブル接続用クエリ
DB_CONNECT = "use "
#   確認用クエリ
DB_LIST         = "show databases"   #   データベース一覧を取得
TABLE_LIST      = "show tables"      #   テーブル一覧を取得
TABLE_DATA_LIST = "select * from "  #   テーブルの中身取得

#   データベース更新用クエリ
TABLE_DATA_UPDATE       = "update "
TABLE_DATA_INSERT       = "insert into "

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
    def set_db_name(self, databbase_name):
        self.db_name = databbase_name
    
    #   テーブル名を設定
    def set_table_name(self, set_table):
        self.table_name = set_table
    
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
    def table_list_display(self, db_name=None):
        if db_name == None:
            db_name = self.db_name
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
    def table_data_list_display(self, db_name=None, table_name=None):
        #   データベース名の引数がなければ
        if db_name == None:
            db_name = self.db_name
        #   テーブル名の引数がなければ
        if table_name == None:
            table_name = self.table_name
        #   テーブル接続
        con = mysql.connector.connect(host = self.host, user = self.user, password = self.password)
        #   カーソルを取得
        cursor = con.cursor()
        try:
            #   接続のSQL文を生成
            connect = DB_CONNECT + db_name
            #   データベース接続
            cursor.execute(connect)
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
            con = mysql.connector.connect(host = self.host, user = self.user, password = self.password)
            try:
                #   カーソルを取得
                cursor = con.cursor()
                #   接続のSQL文を生成
                connect = DB_CONNECT + db_name
                #   データベース接続
                cursor.execute(connect)
                #   指定されたクエリを実行
                result = cursor.execute(query)
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
            con = mysql.connector.connect(host = self.host, user = self.user, password = self.password)
            try:
                #   カーソルを取得
                cursor = con.cursor()
                #   接続のSQL文を生成
                connect = DB_CONNECT + db_name
                #   データベース接続
                cursor.execute(connect)
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
