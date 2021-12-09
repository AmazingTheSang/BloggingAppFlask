import sqlite3
conn = sqlite3.connect('database.db')
cursorObj = conn.cursor()
cursorObj.execute("CREATE TABLE CodeSpeedyBlog(id INTEGER PRIMARY KEY, title VARCHAR(100) NOT NULL , content TEXT NOT NULL, posted_by  VARCHAR(20) NOT NULL,posted_on DATETIME NOT NULL, num_likes INTEGER DEFAULT 0 ) ")
conn.commit()