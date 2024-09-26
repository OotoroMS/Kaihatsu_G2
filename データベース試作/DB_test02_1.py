#db作成 testdb_02=本格的な実験場所
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
cursor.execute("create database testdb_02")


# データベース表示
cursor.execute("show databases")
# すべて取り出し
result = cursor.fetchall()
print("データベース")
for i in result:
    print(i)

# データベースに接続
cursor.execute("use testdb_02")

#テーブル作成
cursor.execute("create table DB_now(id int not null primary key,day varchar(10)"
               +",good_size int,good_vision int,bad_size int,bad_vision int)")
cursor.execute("create table DB_countlog(id int auto_increment not null primary key,day varchar(10)"
               +",good_size int,good_vision int,bad_size int,bad_vision int)")
cursor.execute("create table DB_timelog(id int auto_increment not null primary key,datetime varchar(20)"
               +",type varchar(10))")
cursor.execute("create table DB_sizelog(id int auto_increment not null primary key,datetime varchar(20)"
               +",sizelog float)")

#データ追加
#cursor.execute("insert into DB_now(id,day,good_size,good_vision,bad_size,bad_vision)values(0,curdate(),0,0,0,0)")
cursor.execute("insert into DB_now(id,day,good_size,good_vision,bad_size,bad_vision)values(0,'2024-07-09',1,2,3,4)")#実験用にずれた日付で追加
cursor.execute("insert into DB_countlog(day,good_size,good_vision,bad_size,bad_vision)values(curdate(),5,6,7,8)")
cursor.execute("insert into DB_timelog(datetime,type)values(now(),'size')")
cursor.execute("insert into DB_sizelog(datetime,sizelog)values(now(),3.14)")

conn.commit()

# テーブルの表示
cursor.execute("show tables")
# すべて取り出し
result = cursor.fetchall()
print("テーブル")
for i in result:
    print(i)

cursor.close()