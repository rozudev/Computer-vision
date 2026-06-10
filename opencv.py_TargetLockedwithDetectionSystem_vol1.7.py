import cv2
from cvzone.FaceDetectionModule import FaceDetector
import pyfirmata2
import numpy as np
from sympy import capture

capture = cv2.VideoCapture(0)
ws, hs = 1280, 720
capture.set(3, ws)
capture.set(4, hs)

if not capture.isOpened():
    print("Unable to open video stream")
    exit()

comport = 'COM3'
board = pyfirmata2.Arduino(comport)

servo_pan = board.get_pin('d:9:s') # servo x
servo_tilt = board.get_pin('d:10:s') # servo y
green_led = board.get_pin('d:7:o')
red_led = board.get_pin('d:6:o')
buzzer = board.get_pin('d:8:o')

detector = FaceDetector()
servoPos = [90, 90]

while True:
    success, img = capture.read()
    img, bboxs = detector.findFaces(img, draw=False)

    if bboxs:
        # get coordinates
        fx, fy = bboxs[0]["center"][0], bboxs[0]["center"][1]
        pos = [fx, fy]
        # Convert to servo degree
        servoX = np.interp(fx, [0, ws], [0, 180])
        servoY = np.interp(fy, [0, hs], [0, 180])

        if servoX < 0:
            sevoX = 0
        elif servoX > 180:
            servoX = 180
        if servoY < 0:
            servoY = 0
        elif servoY > 180:
            servoY = 180

        servoPos[0] = servoX
        servoPos[1] = servoY

        cv2.circle(img, (fx, fy), 80, (0, 0, 255), 2)
        cv2.putText(img, str(pos), (fx+15, fy-15), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
        cv2.line(img, (0, fy), (ws, fy), (0, 0, 0), 2) # x line
        cv2.line(img, (fx, hs), (fx, 0), (0, 0, 0), 2) # y line
        cv2.circle(img, (fx, fy), 15, (0, 0, 255), cv2.FILLED)
        cv2.putText(img, "TARGET LOCKED", (850, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
        red_led.write(1)
        buzzer.write(1)
        green_led.write(0)

    else:
        cv2.putText(img, "NO TARGET", (880, 50), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 255), 3)
        cv2.circle(img, (640, 360), 80, (0, 0, 255), 2)
        cv2.circle(img, (640, 360), 15, (0, 0, 255), cv2.FILLED)
        cv2.line(img, (0, 360), (ws, 360), (0, 0, 0), 2) # x line
        cv2.line(img, (640, hs), (640, 0), (0, 0, 0), 2) # y line
        red_led.write(0)
        green_led.write(1)
        buzzer.write(0)

    cv2.putText(img, f'Servo X: {int(servoPos[0])} deg', (50, 50), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
    cv2.putText(img, f'Servo Y: {int(servoPos[1])} deg', (50, 100), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)

    servo_pan.write(servoPos[0])
    servo_tilt.write(servoPos[1])

    cv2.imshow('Target Locked', img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
       break

capture.release()
cv2.destroyAllWindows()





