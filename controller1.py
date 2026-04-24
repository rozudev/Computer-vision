import pyfirmata2
import time

board = pyfirmata2.Arduino('COM5')
time.sleep(2)

led = board.get_pin('d:5:p')

def set_brightness(value):
    """
    value: float between 0.0 and 1.0
    """
    value = max(0,min(1, value))
    led.write(value)