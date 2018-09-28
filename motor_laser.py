import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)

class Servo:
	def __init__(self, pin):
		GPIO.setup(pin, GPIO.OUT)
		self.current_pos = 7.5 # 90 degrees
		self.pwm = GPIO.PWM(pin, self.current_pos)
		self.pwm.start(self.current_pos)

	def move_left(self, degree=10):
		change = degree / 18 + 2.5
		self.current_pos = max(2.5, self.current_pos - change)
		self.pwm.ChangeDutyCycle(self.current_pos)

	def move_right(self, degree=10):
		change = degree / 18 + 2.5
		self.current_pos += change
		self.current_pos = min(12.5, self.current_pos + change)
		self.pwm.ChangeDutyCycle(self.current_pos)

	def move(self, degree=0):
		if degree > 0:
			self.move_right(degree)
		else:
			self.move_left(-degree)

class Laser():
	def __init__(self, pin):
		self.pin = pin
		GPIO.setup(self.pin, GPIO.OUT)
		GPIO,output(self.pin, False)

	def on(self):
		GPIO.output(self.pin, True)

	def off(self):
		GPIO.output(self.pin, False)
