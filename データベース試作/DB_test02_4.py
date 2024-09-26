#db削除
import mysql.connector

# MySQLに接続
conn = mysql.connector.connect(
    host = "172.21.23.51",
    user="testuser",
    password = "is@55870129P"
)

# カーソルを取得
cursor = conn.cursor()
# データベース表示
cursor.execute("show databases")
# すべて取り出し
result = cursor.fetchall()
print("データベース")
for i in result:
    print(i)
#使用    
cursor.execute("use testdb_02")
#削除
cursor.execute("drop database testdb_02")#db
#cursor.execute("drop table db_now")#テーブル
#cursor.execute("delete from db_now where id='0'")#行削除

# データベース表示
cursor.execute("show databases")
# すべて取り出し
result = cursor.fetchall()
print("データベース")
for i in result:
    print(i)

cursor.close()