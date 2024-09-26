#dbテーブル中身確認
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
cursor.execute("use testdb_02")
#cursor.execute("update DB_now set day='2024-7-24',good_size=99,good_vision=95,bad_size=1,bad_vision=4 where id=0")
cursor.execute("insert into DB_countlog(day,good_size,good_vision,bad_size,bad_vision)values(curdate(),5,6,7,8)")
conn.commit()
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
cursor.execute("select * from DB_countlog")
# すべて取り出し
result = cursor.fetchall()
print("中身その2")
for i in result:
    print(i)

# テーブルの中身を表示3
cursor.execute("select * from DB_timelog")
# すべて取り出し
result = cursor.fetchall()
print("中身その3")
for i in result:
    print(i)

# テーブルの中身を表示4
cursor.execute("select * from DB_sizelog")
# すべて取り出し
result = cursor.fetchall()
print("中身その4")
for i in result:
    print(i)

cursor.close()