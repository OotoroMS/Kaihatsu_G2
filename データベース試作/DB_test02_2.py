#db中身調整
import mysql.connector
import datetime
import threading

global tlock #排他制御用変数

# MySQLに接続
tlock=threading.Lock()#排他制御モジュール作成
tlock.acquire()#排他制御開始
conn = mysql.connector.connect(
    host = "172.21.23.51",
    user="testuser",
    password = "is@55870129P"
)

# カーソルを取得
cursor = conn.cursor()

# データベースに接続
cursor.execute("use testdb_02")

#idは自動でインクリメントのため数の指定無しで良い
#DB_nowは更新し続けるためinsertは使わない（id自動インクリメントも無い）
#now()日時,curdate()日付のみ
#float型は小数点第5位まで
#配列の特定の部分に+1する
#num01=i[2]+1
#cursor.execute("insert into DB_now(day,good_size,good_vision,bad_size,bad_vision)values(%d,curdate(),%d,%d,%d,%d)" %(i[0],num01,i[3],i[4],i[5]))
cursor.execute("update DB_now set day='2024-07-24',good_size=99,good_vision=95,bad_size=1,bad_vision=4 where id=0")


# テーブルの中身を取得(日付チェックの為)
# cursor.execute("select * from DB_now")
# result = cursor.fetchall()
# for i in result:
#     num02=i[1]#dayの値を取得

# day=datetime.datetime.today()#現在の日時取得
# d0=day.date()#日付のみ取得
# print("day1")
# print(d0)#new
# print("day2")
# print(num02)#old
# d1=str(d0)#型が違い,判定できないためstrに揃える
# num020=str(num02)
# if num020 != d1:#日付のチェック
#     print("day=no-------------------------")
#     #過去のデータに追加する
#     cursor.execute("insert into DB_countlog(day,good_size,good_vision,bad_size,bad_vision)values('%s',%d,%d,%d,%d)" %(i[1],i[2],i[3],i[4],i[5]))
#     #日付を更新してその他は0から数え直すためリセットする
#     cursor.execute("update DB_now set day='%s',good_size=0,good_vision=0,bad_size=0,bad_vision=0 where id=0" %(d0))

# # テーブルの中身を取得(値を更新する為)
# cursor.execute("select * from DB_now")
# result = cursor.fetchall()
# for i in result:
#     num01=i[2]+1#good_sizeの数を+1する場合
# cursor.execute("update DB_now set good_size = %d where id='0'" %(num01))


# cursor.execute("insert into DB_timelog(datetime,type)values(now(),'size')")
# cursor.execute("insert into DB_timelog(datetime,type)values(now(),'vision')")
conn.commit()

cursor.close()

tlock.release()#排他制御終了