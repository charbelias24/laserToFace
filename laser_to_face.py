import cv2

####### TO BE TESTED ON PI #######

frame_width = 640
frame_height = 480

cascPath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascPath)

camera = PiCamera()
camera.resolution = (frame_width, frame_height)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(frame_width, frame_height))

for frame_temp in camera.capture_continuous(rawCapture, format='bgr', use_video_port=True):
    
    frame = frame_temp.array
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE    
    )

    # Draw a rectangle around the faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

    # Display the resulting frame
    cv2.imshow('Video', frame)
    rawCapture.truncate(0)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()
