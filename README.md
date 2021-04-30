# Laser to Face
Simply shoots laser when it detects a face

### Description
A laser with a rpi-camera mounted on a servo motor, all connected to a Raspberry Pi 3. 
The servo motor rotates randoly until the camera detects a face, then it centers the face in the frame, and enables the laser. 

The face detection is based on Haar-Cascade in OpenCV. 
