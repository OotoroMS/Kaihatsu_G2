#江崎さん試作プログラム
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
cursor.execute("use test")

# テーブルの表示
cursor.execute("show tables")
# すべて取り出し
result = cursor.fetchall()
print("テーブル")
for i in result:
    print(i)

# テーブルの中身を表示
cursor.execute("select * from test")
# すべて取り出し
result = cursor.fetchall()
print("中身その1")
for i in result:
    print(i)

# テーブルに追加
#cursor.execute("insert into test(id, name) value(2,'カテゴリB')")

# 保存を実行
#conn.commit()

# テーブルの中身を表示
cursor.execute("select * from test")
# すべて取り出し
result = cursor.fetchall()
print("中身その2")
for i in result:
    print(i)

# 接続を閉じる
cursor.close()