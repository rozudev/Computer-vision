import pyfirmata2
import time

board = pyfirmata2.Arduino('COM3')
time.sleep(2)

servo = board.get_pin('d:10:s')

def set_servo_angle(angle):
    """
    angle: int from 0 to 180
    """
    angle = max(0,min(180, int(angle)))

    servo.write(angle)