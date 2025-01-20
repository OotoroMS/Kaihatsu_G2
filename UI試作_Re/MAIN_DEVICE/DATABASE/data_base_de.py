import sqlite3
connection = sqlite3.connect("DATABASE\\testdb_main.db")

cursor = connection.cursor()

create_table_query = """
CREATE TABLE IF NOT EXISTS indicator (
id INTEGER PRIMARY KEY AUTOINCREMENT,
calibrate_value REAL NOT NULL
);
"""
drop_table_query = "INSERT INTO indicator (calibrate_value) VALUES (27.00)"
cursor.execute(drop_table_query)

connection.commit()

connection.close()