import sqlite3

connection = sqlite3.connect('data.db')
print("Opened database successfully")
cursor = connection.cursor()
create_table = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY,username TEXT, password TEXT)"
cursor.execute(create_table)

create_table = "CREATE TABLE IF NOT EXISTS items (id INTEGER PRIMARY KEY,name TEXT, price real)"
cursor.execute(create_table)
# cursor.execute("INSERT INTO items VALUES ('test',10.99)")
connection.commit()
connection.close()
