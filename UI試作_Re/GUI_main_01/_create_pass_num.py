from parts.SQLCommunication_main import SQLCommunication

# テーブル作成クエリ
delete_table = "DROP TABLE IF EXISTS pass_num"
create_table_query = "CREATE TABLE IF NOT EXISTS pass_num ( id INTEGER PRIMARY KEY AUTOINCREMENT, num TEXT NOT NULL)"
set_password_query = "INSERT INTO pass_num (num) VALUES (\"2024\")"
db = SQLCommunication()
db.db_query_execution("testdb_main.db", delete_table)
db.db_query_execution("testdb_main.db", create_table_query)

db.db_query_execution("testdb_main.db",set_password_query)
db.db_list_display
print("end")