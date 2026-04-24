import cv2
from cvzone.HandTrackingModule import HandDetector
import controller1 as cnt
import math

detector = HandDetector(detectionCon=0.8,maxHands=1)
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    hands, img = detector.findHands(frame)
    brightness = 0.0

    if hands:
        lmList = hands[0]['lmList']

        # Thumb tip & index tip
        x1, y1 = lmList[4][:2]
        x2, y2 = lmList[8][:2]

        # Distance
        length = math.hypot(x2-x1, y2-y1)

        # Map distance to brightness
        min_dist = 30
        max_dist = 200

        brightness = (length - min_dist) / (max_dist - min_dist)
        brightness = max(0, min(1, brightness))
        cnt.set_brightness(brightness)


    cv2.putText(
        img,
        f'Brightness: {int(brightness * 100)}%',
        (20, 50),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2
    )
    cv2.imshow("LED Brightness Control", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
       break

