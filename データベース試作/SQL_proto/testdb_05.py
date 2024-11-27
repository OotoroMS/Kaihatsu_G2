# csv形式で取り出す 横に長い,まとまってる,微妙
import sqlite3
import csv
# SQLiteに接続（データベースファイルを作成または開く）
conn = sqlite3.connect("D:\\GitHub\\Kaihatsu_G2\\データベース試作\\SQL_proto\\testdb_main.db")

# カーソルを取得
cursor = conn.cursor()
tables = ['DB_now', 'DB_countlog', 'DB_sizelog', 'DB_timelog']
#内容記述
with open("D:\\GitHub\\Kaihatsu_G2\\データベース試作\\SQL_proto\\export.csv",'w')as f:
    writer=csv.writer(f)

    for i in tables:
        cursor.execute("SELECT * FROM {};".format(i))
        rows = cursor.fetchall()
        writer.writerow(rows)

# カーソルと接続をクローズ
cursor.close()
conn.close()