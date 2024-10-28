#mainDB中身確認
import sqlite3

# SQLiteに接続（データベースファイルを作成または開く）
conn = sqlite3.connect("D:\\GitHub\\Kaihatsu_G2\\データベース試作\\SQL_proto\\testdb_main.db")

# カーソルを取得
cursor = conn.cursor()

# データベース（SQLiteはファイルベースなので作成不要）

# データの更新: idが0のレコードのgood_sizeを10に、bad_sizeを20に更新
cursor.execute("""
    UPDATE DB_now
    SET good_size = ?, bad_size = ?
    WHERE id = ?
    """, (10, 20, 0))  # ?の部分に新しい値を渡す

# コミットして変更を保存
conn.commit()

# テーブルの表示
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
result = cursor.fetchall()
print("テーブル")
for i in result:
    print(i)

# カーソルと接続をクローズ
cursor.close()
conn.close()
