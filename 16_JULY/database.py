import sqlite3

conn = sqlite3.connect('py4e.db')
cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS Counts')
cur.execute('''
CREATE TABLE counts (email TEXT, count INTEGER) ''')

with open('mbox.txt', 'r') as file:
    for line in file:
        if not line.startswith('From:'): continue
        pieces = line.split()
        email = pieces[1]
        cur.execute('SELECT count FROM counts WHERE email = ?', (email,))
        row = cur.fetchone()

        if row is None:
            cur.execute('''INSERT INTO counts (email,count) VALUES (?,1)''', (email,))
        else:
            cur.execute('UPDATE counts SET count = count+1 WHERE email = ?',(email,))
        conn.commit()

sqlstr = 'SELECT count, email FROM counts ORDER BY count DESC LIMIT 10'

for row in cur.execute(sqlstr):
    print(str(row[0]), row[1])

cur.close()