#db中身調整実験
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

#idは自動でインクリメントのため数の指定無しで良い
#DB_nowは更新し続けるためinsertは使わない（id自動インクリメントも無い）
#now()日時,curdate()日付のみ
#float型は小数点第5位まで
#cursor.execute("insert into DB_now(day,good_size,good_vision,bad_size,bad_vision)values(curdate(),1,2,3,4)")
#cursor.execute("insert into DB_sizelog(datetime,sizelog)values(now(),3.14159)")
#conn.commit()

# テーブルの中身を選択
cursor.execute("select * from DB_now")
result = cursor.fetchall()
for i in result:
    num01=i[2]+1

#配列の特定の部分に+1する
#num01=i[2]+1
#cursor.execute("insert into DB_now(day,good_size,good_vision,bad_size,bad_vision)values(%d,curdate(),%d,%d,%d,%d)" %(i[0],num01,i[3],i[4],i[5]))
cursor.execute("update DB_now set good_size = %d where id='0'" %(num01))
conn.commit()

# テーブルの中身を表示1
cursor.execute("select * from DB_now")
result = cursor.fetchall()
print("中身その1")
for i in result:
    print(i)

cursor.close()