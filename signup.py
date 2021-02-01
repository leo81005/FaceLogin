import cv2
import sqlite3

conn = sqlite3.connect("vip_member.sqlite")
cursor = conn.cursor()
sqlstr = 'select * FROM member'
cursor.execute(sqlstr)

rows = cursor.fetchall()
member = []
for row in rows:
    member.append(row[0])
while True:
    memberid = input("請輸入帳號:")
    if memberid == '':
        break
    elif memberid in member:
        print('此帳號已存在')
    else:
        imgfile = memberid + '.jpg'
        cv2.namedWindow("frame")
        cap = cv2.VideoCapture(0)
        while (cap.isOpened()):
            ret, img = cap.read()
            if ret == True:
                cv2.imshow("frame", img)
                # k = cv2.waitKey(0)
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    cv2.imwrite('memberPic/' + imgfile, img)
                    cv2.destroyAllWindows()
                    break
        cap.release()

        sqlstr = 'INSERT INTO member values("{}", "{}")'.format(memberid, imgfile)
        cursor.execute(sqlstr)
        conn.commit()
        print('帳號建立成功')

conn.close()

