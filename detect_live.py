import os
import cv2
platecascade = cv2.CascadeClassifier(os.path.join(os.path.dirname(os.path.abspath(__file__)), "haarcascade_russian_plate_number.xml"))
minArea = 500
cap = cv2.VideoCapture (0)
count = 0
while True:
    success, img= cap.read ( )
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
    numberplates = platecascade.detectMultiScale(imgGray, 1.1, 4)
    for (x, y, w, h) in numberplates:
        area = w * h
        if area > minArea:
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
            # here we are making a rectangle around the number plate detecting in our image
            cv2.putText(img, "NUMBER PLATE", (x, y - 5), cv2.FONT_HERSHEY_COMPLEX, 1, (8, 0, 255), 2)
            # here we are putting the text over the detected plate
            imgRoi = img[y:y + h, x:x + w]
            # here we are defing our region of Interest
            cv2.imshow("ROI", imgRoi)
            # displaying our region of interest
    cv2.imshow("RESULT", img)
    if cv2.waitKey(1) & 0xFF == ord('s'):
                                                                                        # pressing S will save the dectected number plate
        cv2.imwrite("/Users/yuvrajchawla/Desktop/z Number Plate/IMAGES" + str(count) + ".jpg", imgRoi)
    # here we have defined where our image will
        cv2.rectangle(img, (0,200), (640, 300), (255,8,8),cv2.FILLED)
        cv2.putText(img, "SCAN SAVED", (15,265), (8,255,255),2)
                                                                                       # after pressing S this will display SCAN SAVED on the screen
        cv2.imshow( "RESULT", img)
        cv2.waitKey(500)
        count = count + 1


