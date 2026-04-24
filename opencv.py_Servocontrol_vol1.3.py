import cv2
import mediapipe as mp
import math
import controller3 as cnt

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

min_dist = 0.02
max_dist = 0.20

while True:
    success, img = cap.read()
    if not success:
        break

    img = cv2.flip(img, 1)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    result = hands.process(img_rgb)

    angle = 0

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:

            # Get landmarks
            thumb_tip = hand_landmarks.landmark[4]
            index_tip = hand_landmarks.landmark[8]

            h, w, _ = img.shape
            x1, y1 = int(thumb_tip.x * w), int(thumb_tip.y * h)
            x2, y2 = int(index_tip.x * w), int(index_tip.y * h)

            # DRAW STICK
            cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 3)
            cv2.circle(img, (x1, y1), 8, (255, 0, 255), -1)
            cv2.circle(img, (x2, y2), 8, (255, 0, 255), -1)


            dist = math.hypot(thumb_tip.x - index_tip.x,
                              thumb_tip.y - index_tip.y)

            # MAP distance → angle
            angle = (dist - min_dist) / (max_dist - min_dist)
            angle = max(0, min(1, angle))
            angle = angle * 180

            # Send to servo
            cnt.set_servo_angle(angle)

            # Draw hand landmarks
            mp_draw.draw_landmarks(
                img,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS
            )

    # Show angle
    cv2.putText(
        img,
        f'Angle: {int(angle)}',
        (20, 50),
        cv2.FONT_HERSHEY_SIMPLEX,
        1.2,
        (0, 255, 255),
        3
    )

    cv2.imshow("Hand Servo Control", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()



