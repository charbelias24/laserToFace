import RPi.GPIO as GPIO

servo = 3
laser = 5

GPIO.setmode(GPIO.BOARD)
GPIO.setup(servo, GPIO.OUT)
GPIO.setup(laser, GPIO,OUT)

