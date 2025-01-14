from parts.SQLCommunication_main import SQLCommunication

db = SQLCommunication()
db.set_db_name("testdb_main.db")

db.db_query_execution(query="DELETE FROM db_countlog")
db.db_query_execution(query="DELETE FROM db_timelog")
