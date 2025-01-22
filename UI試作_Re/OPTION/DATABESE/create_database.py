import sqlite3

# データベース接続(生成)
conn = sqlite3.connect("D:\\Kaihatsu\\OPTION_py311\\DATABESE\\DB_option.db")

# カーソル生成
cursor = conn.cursor()

# テーブルを生成
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
        datetime TEXT,
        bad_vision_path TEXT,
        bad_mark_path   TEXT
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS pass_num(
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        num TEXT
    )
""")

# コミットして変更を保存
conn.commit()
