import cv2
from picamera import PiCamera
from picamera.array import PiRGBArray
from motor_laser import *

####### TO BE TESTED ON PI #######

class LaserToFace:
    def __init__(self, frame_width=640, frame_height=480, servo_x=3, servo_y=5, laser=7, speed_control=1, laser_face_distance=50):
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.frame_center_x = frame_width / 2
        self.frame_center_y = frame_height / 2
        self.laser_face_distance = laser_face_distance
        self.speed_control = speed_control # The higher the faster the servo will move towards the face

        self.cascPath = "haarcascade_frontalface_default.xml"
        self.faceCascade = cv2.CascadeClassifier(self.cascPath)

        self.camera = PiCamera()
        self.camera.resolution = (frame_width, frame_height)
        self.camera.framerate = 32
        self.rawCapture = PiRGBArray(self.camera, size=(frame_width, frame_height))

        self.servo_x = Servo(pin=servo_x)
        self.servo_y = Servo(pin=servo_y)
        self.laser = Laser(pin=laser)

    def start(self):
        for frame_temp in self.camera.capture_continuous(self.rawCapture, format='bgr', use_video_port=True):
            self.detect(frame_temp.array)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # When everything is done, release the capture
        cv2.destroyAllWindows()

    def detect(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        cv2.circle(frame, (int(self.frame_center_x), int(self.frame_center_y)), 2, (0,255,255),2)
        
        faces = self.faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30),
            flags=cv2.CASCADE_SCALE_IMAGE    
        )

        # Draw a rectangle around the faces
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        # Move the servo until the face is in the center of the frame
        if len(faces):
            (x, y, w, h) = faces[0]
            # Draw a red rectangle around the first face
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)
            

            center_face_x = x + w / 2
            center_face_y = y + h / 2
            cv2.circle(frame, (int(center_face_x), int(center_face_y)), 2, (0,255,255),2)
            
            print("[FACE] X:{}, Y:{}".format(center_face_x, center_face_y))
            difference_x = self.frame_center_x - center_face_x
            difference_y = self.frame_center_y - center_face_y
            print("[DISTANCE TO FACE] X:{}, Y:{}".format(difference_x, difference_y))

            # Check if the center of the screen is in the sqaure of the face 
            if not abs(difference_x) < w / 2:
                self.servo_x.move(difference_x)
            if not abs(difference_y) < h / 2:
                self.servo_y.move(-difference_y)   

            if abs(difference_y) < self.laser_face_distance and abs(difference_x) < self.laser_face_distance:
                self.laser.on()
            else:
                self.laser.on()

        # Display the resulting frame
        cv2.imshow('Video', frame)
        self.rawCapture.truncate(0)

