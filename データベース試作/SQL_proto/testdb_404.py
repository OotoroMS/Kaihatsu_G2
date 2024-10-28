#DB削除
import os

# データベースファイルのパス
db_path = "D:\\GitHub\\Kaihatsu_G2\\データベース試作\\SQL_proto\\testdb_option.db"

# データベースファイルが存在するか確認
if os.path.exists(db_path):
    # データベースファイルを削除
    os.remove(db_path)
    print(f"{db_path} を削除しました。")
else:
    print(f"{db_path} が存在しません。")