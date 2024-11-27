# csv形式で取り出す_03 縦長,データ分かれてる, 成功
import sqlite3
import csv
# SQLiteに接続（データベースファイルを作成または開く）
conn = sqlite3.connect("D:\\GitHub\\Kaihatsu_G2\\データベース試作\\SQL_proto\\testdb_main.db")

# カーソルを取得
cursor = conn.cursor()
tables = ["DB_now", "DB_countlog", "DB_sizelog", "DB_timelog"]
#内容記述
with open("D:\\GitHub\\Kaihatsu_G2\\データベース試作\\SQL_proto\\export.csv",'w')as f:
    writer=csv.writer(f)
    num = -1
    for i in tables:
        num += 1
        cursor.execute("SELECT * FROM {};".format(i))
        rows = cursor.fetchall()
        writer.writerow([tables[num] + ' ----------------------------------------------------------------------'])
        for j in rows:
            j_list = list(j)
            for k in range(len(j_list)):
                if type(j_list[k]) is int:
                    j_list[k] = str(j_list[k])
                elif j_list[k] is None:
                    j_list[k] = ""
                elif type(j_list[k]) is float:
                    j_list[k] = str(j_list[k])
            writer.writerow(list(j_list))
# カーソルと接続をクローズ
cursor.close()
conn.close()