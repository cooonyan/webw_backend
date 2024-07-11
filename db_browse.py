import sqlite3

conn = sqlite3.connect('userdata.db')
cursor = conn.cursor()
# cursor.execute('INSERT INTO "user-information" (username) VALUES (?)', ('user-public-token',))
# conn.commit
cursor.execute('SELECT * FROM "user-information"')
print(cursor.fetchall())
conn.close
