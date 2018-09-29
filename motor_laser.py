import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BOARD)

def translate(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)

class Servo:
	def __init__(self, pin):
                GPIO.setup(pin, GPIO.OUT)
                self.current_pos = 7.5 # 90 degrees
                self.pwm = GPIO.PWM(pin, 50)
                self.pwm.start(self.current_pos)

	def move_right(self, degree=10):
		change = degree / 18
		self.current_pos = max(2.5, self.current_pos - change)
		self.pwm.ChangeDutyCycle(self.current_pos)
		print("[SERVO] Moving left")
		print("[SERVO] Current position:", self.current_pos) 

	def move_left(self, degree=10):
		change = degree / 18
		self.current_pos = min(12.5, self.current_pos + change)
		self.pwm.ChangeDutyCycle(self.current_pos)
		print("[SERVO] Moving right")
		print("[SERVO] Current position:", self.current_pos)

	def move(self, degree=0):
		if degree >= 60:
			self.move_right(translate(degree, 0, 400, 0, 20))
		elif degree <= -60:
			self.move_left(translate(-degree, 0, 400, 0, 20))
		sleep(0.1)

class Laser():
	def __init__(self, pin):
		self.pin = pin
		GPIO.setup(self.pin, GPIO.OUT)
		GPIO.output(self.pin, False)

	def on(self):
		GPIO.output(self.pin, True)
		print("[LASER] ON")

	def off(self):
		GPIO.output(self.pin, False)
		print("[LASER] OFF")
