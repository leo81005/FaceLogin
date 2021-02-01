import cv2
import sqlite3
import requests
from json import JSONDecoder
import time
import face_recognition
from datetime import datetime


def compareimage(filepath1, filepath2):
    try:
        image1 = cv2.imread(filepath1)
        rgb1 = cv2.cvtColor(image1, cv2.COLOR_BGR2RGB)

        boxes1 = face_recognition.face_locations(image1)
        encodings1 = face_recognition.face_encodings(image1, boxes1)[0]

        image2 = cv2.imread(filepath2)
        rgb2 = cv2.cvtColor(image2, cv2.COLOR_BGR2RGB)

        boxes2 = face_recognition.face_locations(image2)
        encodings2 = face_recognition.face_encodings(image2, boxes2)[0]

        matches = face_recognition.compare_faces([encodings1], encodings2)[0]
        face_distances = face_recognition.face_distance([encodings1], encodings2)
        print("差異度:", face_distances)
        return face_distances
    except Exception:
        print("產生錯誤，無法識別")
        return 0


conn = sqlite3.connect('vip_member.sqlite')
cursor = conn.cursor()
sqlstr = 'SELECT * FROM member'
cursor.execute(sqlstr)
rows = cursor.fetchall()
imagedict = {}
for row in rows:
    imagedict[row[0]] = 'memberPic/' + row[1]

timenow = time.time()
cv2.namedWindow("frame")
cap = cv2.VideoCapture(0)
while(cap.isOpened()):
    count = 5 - int(time.time() - timenow)
    ret, img = cap.read()
    if ret == True:
        imgcopy = img.copy()
        cv2.putText(imgcopy, str(count), (200,400), cv2.FONT_HERSHEY_SIMPLEX, 15, (0,0,255), 35)
        cv2.imshow("frame", imgcopy)
        k = cv2.waitKey(100)
        if k == ord("z") or k == ord("Z") or count == 0:
            cv2.imwrite("temp/temp.jpg", img)
            break
cap.release()
cv2.destroyWindow("frame")

success = True
grade = []
name = []
for img in imagedict:
    print(img)
    grade.append(compareimage(imagedict[img], "temp/temp.jpg"))
    name.append(img)

if min(grade)>0.5:
    success = False
    print('登入失敗！你可能不是會員！ 或嘗試重拍照')
else:
    print('登入成功！歡迎 ' + name[grade.index(min(grade))] + '！' )
    savetime = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    sqlstr = 'INSERT INTO login values("{}","{}")'.format(img, savetime)
    cursor.execute(sqlstr)
    conn.commit()


conn.close()
