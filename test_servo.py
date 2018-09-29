import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setup(3, GPIO.OUT)
p = GPIO.PWM(3, 50)
p.start(7.5)
while True:
    for i in [x * 0.1 for x in range(25, 125)]:
        p.ChangeDutyCycle(i)
        time.sleep(0.1)
