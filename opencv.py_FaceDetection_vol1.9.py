import cv2
from cvzone.FaceDetectionModule import FaceDetector
import pyfirmata2

capture = cv2.VideoCapture(0)
ws, hs = 900, 600
capture.set(3, ws)
capture.set(4, hs)

comport = 'COM3'
board = pyfirmata2.Arduino(comport)

led_green = board.get_pin('d:8:o')
led_red = board.get_pin('d:7:o')
buzzer = board.get_pin('d:9:o')

detector = FaceDetector()

while True:
    success, img = capture.read()
    img, bboxs = detector.findFaces(img)

    if bboxs:
        led_green.write(1)
        led_red.write(0)
        buzzer.write(0)

    else:
        led_green.write(0)
        led_red.write(1)
        buzzer.write(1)

    cv2.imshow('Face detector', img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

capture.release()
cv2.destroyAllWindows()

