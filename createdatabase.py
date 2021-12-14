import sqlite3
conn = sqlite3.connect('database.db')
cursorObj = conn.cursor()
cursorObj.execute("DROP TABLE User")
conn.commit()