import os
import cv2
import datetime

platecascade = cv2.CascadeClassifier(os.path.join(os.path.dirname(os.path.abspath(__file__)), "haarcascade_russian_plate_number.xml"))
minArea = 500
OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "captures")
os.makedirs(OUT_DIR, exist_ok=True)
cap = cv2.VideoCapture(0)
count = 0

while True:
    success, img = cap.read()
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    numberplates = platecascade.detectMultiScale(imgGray, 1.1, 4)

    for (x, y, w, h) in numberplates:
        area = w * h
        if area > minArea:
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
            cv2.putText(img, "NUMBER PLATE", (x, y - 5), cv2.FONT_HERSHEY_COMPLEX, 1, (8, 0, 255), 2)
            img_roi = img[y:y + h, x:x + w] # create a new variable to store the region of interest
            ts = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S-%f")
            filename = os.path.join(OUT_DIR, f"plate_{ts}.jpg") # generate a unique filename based on the timestamp
            cv2.imshow("ROI", img_roi)
            cv2.imwrite(filename, img_roi) # save the region of interest as a new image with the unique filename
            count += 1

    cv2.imshow("RESULT", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
