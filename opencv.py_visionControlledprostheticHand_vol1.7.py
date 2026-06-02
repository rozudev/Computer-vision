import cv2
import mediapipe as mp
import pyfirmata2
import time

board = pyfirmata2.Arduino('COM3')
time.sleep(2)

# Servo pins
servo1_thumb = board.get_pin('d:9:s')
servo2_index = board.get_pin('d:10:s')
servo3_middle = board.get_pin('d:11:s')
servo3_ring = board.get_pin('d:12:s')
servo4_pinky = board.get_pin('d:13:s')

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7,
)

mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

def move_servo(servo, state):
    if state == 1:
        servo.move(180)
    else:
        servo.move(0)

while True:
    succes, img = cap.read()
    if not succes:
        break

    img = cv2.flip(img, 1)
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:

            mp_draw.draw_landmarks(img, handLms, mp_hands.HAND_CONNECTIONS)
            lmList = h, w, c = img.shape

            for id, lm in enumerate(handLms.landmark):
                cx, cy = int(lm.x*w), int(lm.y*h)
                lmList = [cx, cy]

            if len(lmList) != 0:
                fingers = []

                if lmList[4][0]>lmList[3][0]:
                    fingers.append(1)
                else:
                    fingers.append(0)

                tips = [8, 12, 16, 20]

                for tip in tips:
                    if lmList[tip][1]<lmList[tip-2][1]:
                        fingers.append(1)
                    else:
                        fingers.append(0)


                move_servo(servo1_thumb,finger[0])
                move_servo(servo2_index,finger[1])
                move_servo(servo3_middle,finger[2])
                move_servo(servo3_ring,finger[3])
                move_servo(servo4_pinky,finger[4])

    print("Fingers:", fingers)
    cv.imshow('Hand Tracking', img)

    if cv2.waitKey(1) & 0xFF == 27:
        break
    time.sleep(0.02)

cap.release()
cv2.destroyAllWindows()
