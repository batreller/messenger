import sqlite3

conn = sqlite3.connect('users.db', isolation_level=None)
cur = conn.cursor()

cur.execute("INSERT INTO users VALUES(-1, 'test', 'test', 'test', 'test');")
