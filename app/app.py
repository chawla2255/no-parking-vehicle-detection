import os
import cv2
from flask import Flask, render_template, Response

app = Flask(__name__)

platecascade = cv2.CascadeClassifier(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../haarcascade_russian_plate_number.xml"))
minArea = 1000
cap = cv2.VideoCapture(0)

@app.route('/')
def index():
    return render_template('index.html')

def gen_frames():
    found_plate = False
    last_frame = None

    while True:
        success, img = cap.read()
        if not success:
            break
        else:
            imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
            # imgGray = cv2.equalizeHist(imgGray)
            # numberplates = platecascade.detectMultiScale(imgGray, 1.1, 4)
            numberplates = platecascade.detectMultiScale(imgGray, scaleFactor=1.1, minSize=(100, 100))

            for (x, y, w, h) in numberplates:
                area = w * h
                if area > minArea:
                    found_plate = True
                    # cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    cv2.putText(img, "NUMBER PLATE", (x, y - 10), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 255, 0), 2)
                    imgRoi = img[y:y + h, x:x + w]
                    ret, buffer = cv2.imencode('.jpg', imgRoi)
                    imgRoi = buffer.tobytes()
                    yield (b'--frame\r\n'
                           b'Content-Type: image/jpeg\r\n\r\n' + imgRoi + b'\r\n')
            
            if not found_plate:
                last_frame = img
                ret, buffer = cv2.imencode('.jpg', img)
                img = buffer.tobytes()
                yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + img + b'\r\n')
            else:
                break
            
    if last_frame is not None:
        ret, buffer = cv2.imencode('.jpg', last_frame)
        img = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + img + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)