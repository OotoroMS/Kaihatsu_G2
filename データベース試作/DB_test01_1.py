#db作成実験 testdb_01=実験場所
import mysql.connector

# MySQLに接続
conn = mysql.connector.connect(
    host = "172.21.23.51",
    user="testuser",
    password = "is@55870129P"
)

# カーソルを取得
cursor = conn.cursor()

# データベース作成
cursor.execute("create database testdb_01")


# データベース表示
cursor.execute("show databases")
# すべて取り出し
result = cursor.fetchall()
print("データベース")
for i in result:
    print(i)

# データベースに接続
cursor.execute("use testdb_01")

cursor.execute("create table DB_now(id int not null primary key,day varchar(10)"
               +",good_size int,good_vision int,bad_size int,bad_vision int)")
cursor.execute("create table DB_sizelog(id int auto_increment not null primary key,datetime varchar(20)"
               +",sizelog float)")

#cursor.execute("insert into DB_now(id,day,good_size,good_vision,bad_size,bad_vision)values(0,curdate(),0,0,0,0)")
cursor.execute("insert into DB_now(id,day,good_size,good_vision,bad_size,bad_vision)values(0,'2024-07-09',0,0,0,0)")#実験用にずれた日付で追加
cursor.execute("insert into DB_sizelog(id,datetime,sizelog)values(0,now(),0)")

conn.commit()

# テーブルの表示
cursor.execute("show tables")
# すべて取り出し
result = cursor.fetchall()
print("テーブル")
for i in result:
    print(i)

#テーブル確認
#!!!!!cursor.execute("describe testDB_02")

# テーブルの中身を表示
#cursor.execute("select * from test")

# すべて取り出し
#result = cursor.fetchall()
#print("中身その1")
#for i in result:
#    print(i)

# テーブルに追加
#cursor.execute("insert into test(id, name) value(2,'カテゴリB')")

# 保存を実行
#conn.commit()

# テーブルの中身を表示
#cursor.execute("select * from test")
# すべて取り出し
#result = cursor.fetchall()
#print("中身その2")
#for i in result:
#    print(i)

# 接続を閉じる
cursor.close()