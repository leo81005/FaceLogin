import sqlite3

conn = sqlite3.connect('vip_member.sqlite')
cursor = conn.cursor()
sqlstr = 'SELECT * FROM login'
cursor.execute(sqlstr)
rows = cursor.fetchall()
print('%-15s %-20s' % ('帳號','登入時間'))
print('=============== ====================')
for row in rows:
    print('%-15s %-20s' % (row[0], row[1]))

conn.close()