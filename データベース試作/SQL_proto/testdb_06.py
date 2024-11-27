# csv形式で取り出す_02　ターミナルからコピペしないといけない　微妙
import sqlite3

# SQLiteに接続（データベースファイルを作成または開く）
conn = sqlite3.connect("D:\\GitHub\\Kaihatsu_G2\\データベース試作\\SQL_proto\\testdb_main.db")

# カーソルを取得
cursor = conn.cursor()

tables = ['DB_now', 'DB_countlog', 'DB_sizelog', 'DB_timelog']

for i in tables:
    cursor.execute("SELECT * FROM {};".format(i))
    rows = cursor.fetchall()
    print(i + ' ------------------------------------------------------')
    for j in rows:
        j_list = list(j)
        for k in range(len(j_list)):
            if type(j_list[k]) is int:
                j_list[k] = str(j_list[k])
            elif j_list[k] is None:
                j_list[k] = ""
            elif type(j_list[k]) is float:
                j_list[k] = str(j_list[k])
        print(','.join(list(j_list)))

# カーソルと接続をクローズ
cursor.close()
conn.close()