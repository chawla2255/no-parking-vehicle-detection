# Vehicle detection in no-parking zones

A real-time computer vision prototype that spots vehicles in restricted zones (bus stops, fire lanes,
loading bays) by detecting their number plates on a live camera feed, capturing each plate for review.
Built as a B.Tech project-based-learning module at Manipal University Jaipur (Feb to Nov 2023).

## How it works

1. Frames come from a webcam or CCTV stream (`cv2.VideoCapture`).
2. Each frame is converted to grayscale and scanned with a Haar cascade trained on licence plates.
3. Detections larger than a minimum area are boxed and labelled on screen.
4. The plate region is cropped and saved with a timestamp, ready to be matched against a no-parking zone
   and sent to an enforcement queue.

| File | What it is |
| --- | --- |
| `detect_live.py` | Live detection with on-screen boxes |
| `detect_and_capture.py` | Live detection that saves every plate crop to `captures/` with a timestamp |
| `app/app.py` | Flask web app that streams the camera and returns the first plate it finds |

## Run it

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python detect_and_capture.py          # press q to quit
python app/app.py                     # then open http://127.0.0.1:5000
```

## Next steps

- Swap the Haar cascade for a CNN detector (YOLO) to cut false positives at night and at angles
- Add OCR on the crops and a geofence check so only vehicles inside a no-parking polygon raise an alert

## Credits

- Built by **Yuvraj Chawla** with **Ananya** (Manipal University Jaipur).
- The detection loop follows the standard OpenCV Haar-cascade number-plate approach from public tutorials.
- `haarcascade_russian_plate_number.xml` ships with [OpenCV](https://github.com/opencv/opencv) and keeps its
  original Intel/OpenCV license.

MIT License for the code in this repository.
