#optionDB作成
import sqlite3

# SQLiteに接続（データベースファイルを作成または開く）
conn = sqlite3.connect("D:\\GitHub\\Kaihatsu_G2\\データベース試作\\SQL_proto\\testdb_option.db")

# カーソルを取得
cursor = conn.cursor()

# データベース（SQLiteはファイルベースなので作成不要）

# テーブル作成
cursor.execute("""
    CREATE TABLE IF NOT EXISTS DB_now(
        id INTEGER NOT NULL PRIMARY KEY,
        day TEXT,
        good_vision INTEGER,
        bad_vision INTEGER
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS DB_countlog(
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        day TEXT,
        good_vision INTEGER,
        bad_vision INTEGER
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS DB_timelog(
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        datetime TEXT
    )
""")

# データ追加
cursor.execute("""
    INSERT INTO DB_now(id, day, good_vision, bad_vision)
    VALUES(0, '2024-10-20', 1, 2)
""")  # 実験用にずれた日付で追加

cursor.execute("""
    INSERT INTO DB_countlog(day, good_vision, bad_vision)
    VALUES(date('now'), 5, 6)
""")

cursor.execute("""
    INSERT INTO DB_timelog(datetime)
    VALUES(datetime('now'))
""")

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
