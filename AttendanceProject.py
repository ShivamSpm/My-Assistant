import cv2
import numpy as np
import face_recognition as fr
import os
from datetime import datetime


class Recognition:

    path = 'images'
    images = []
    classNames = []
    myList = os.listdir(path)
    for cl in myList:
        curImg = cv2.imread(f'{path}/{cl}')
        images.append(curImg)
        classNames.append(os.path.splitext(cl)[0])

    encodeListKnown = []
    for img in images:
        img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        encode = fr.face_encodings(img)[0]
        encodeListKnown.append(encode)

    # def markAttendance(name):
    #     with open('Attendance.csv','r+') as f:
    #         myDataList = f.readlines()
    #         nameList = []
    #         for line in myDataList:
    #             entry = line.split(',')
    #             nameList.append(entry[0])
    #         if name not in nameList:
    #             now = datetime.now()
    #             dtString = now.strftime('%H:%M:%S')
    #             f.writelines(f'\n{name},{ dtString}')
    # encodeListKnown = findEncodings(images)
    print('Encoding Done')


    def match(self):
        cap = cv2.VideoCapture(0)
        while True:
            success, img = cap.read()
            imgS = cv2.resize(img,(0,0), None,0.25,0.25)
            imgS = cv2.cvtColor(imgS,cv2.COLOR_BGR2RGB)

            facesCurFrame = fr.face_locations(imgS)
            encodesCurFrame = fr.face_encodings(imgS,facesCurFrame)
            for encodeFace in encodesCurFrame:
                matches = fr.compare_faces(self.encodeListKnown,encodeFace)
                faceDis = fr.face_distance(self.encodeListKnown,encodeFace)

                matchIndex = np.argmin(faceDis)

                if matches[matchIndex]:
                    name = self.classNames[matchIndex].upper()
                    # y1,x2,y2,x1 = faceLoc
                    # y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
                    # cv2.rectangle(img, (x1, y1),
                    #               (x2, y2), (255, 0, 255), 2)
                    # cv2.rectangle(img,(x1, y2-35),
                    #               (x2, y2), (0, 255, 0), cv2.FILLED)
                    # cv2.putText(img,name,(x1+6, y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
                    # markAttendance(name)
                    return name

                    # print(name)


# def main():
#     recog = Recognition()
#     name = recog.match()
#     print(name)
#
#
# if __name__ == '__main__':
#     main()


    # cv2.imshow('Webcam', img)
    # cv2.waitKey(1)

