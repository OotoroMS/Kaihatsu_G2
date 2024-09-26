#dbテーブル中身確認実験
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

# データベースに接続
cursor.execute("use testdb_01")

# テーブルの表示
cursor.execute("show tables")
# すべて取り出し
result = cursor.fetchall()
print("テーブル")
for i in result:
    print(i)

# テーブルの中身を表示1
cursor.execute("select * from DB_now")
# すべて取り出し
result = cursor.fetchall()
print("中身その1")
for i in result:
    print(i)

# テーブルの中身を表示2
cursor.execute("select * from DB_sizelog")
# すべて取り出し
result = cursor.fetchall()
print("中身その2")
for i in result:
    print(i)

cursor.close()