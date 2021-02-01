import sqlite3

conn = sqlite3.connect('vip_member.sqlite')
cursor = conn.cursor()
sqlstr = 'CREATE TABLE IF NOT EXISTS member("memberid" TEXT, "picture" "TEXT")'
cursor.execute(sqlstr)
sqlstr = 'CREATE TABLE IF NOT EXISTS login("memberid" TEXT, "picture" "TEXT")'
cursor.execute(sqlstr)

conn.commit()

conn.close