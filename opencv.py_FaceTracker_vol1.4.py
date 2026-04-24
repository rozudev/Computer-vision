import cv2
import time
import serial

# Connection
arduinoData = serial.Serial('COM3', 115200)
time.sleep(2)

prev_x, prev_y = 320, 240
alpha = 0.2

def smooth(new, prev):
    return int(prev + alpha*(new - prev))
def send_coordinates(x, y):
    data = f"{x},{y}\n"
    arduinoData.write(data.encode())

# Camera setup
capture = cv2.VideoCapture(0)
capture.set(3, 640) # width
capture.set(4, 480)  # height

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

while True:
    ret, frame = capture.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.05, 8, minSize=(125, 125))

    for (x, y, w, h) in faces:
        cx = x + w // 2
        cy = y + h // 2

        cx = smooth(cx, prev_x)
        cy = smooth(cy, prev_y)
        prev_x, prev_y = cx, cy

        # Send to arduino
        send_coordinates(cx, cy)

        # Rectangle and circle
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.circle(frame, (cx, cy), 5, (0, 0, 255), -1)

    cv2.imshow('Face Tracker', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

capture.release()
cv2.destroyAllWindows()
