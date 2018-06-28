from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import sys
import imutils

# Get user supplied values
cascPath1 = '/home/pi/Desktop/otto/face-models/haarcascade_frontalface_default.xml'
cascPath2= '/home/pi/Desktop/otto/face-models/haarcascade_profileface.xml'

def detectFaces(camera_stop):
    try:
        print("comecooo")
        #block execution while no signal arrives
        camera_stop.get()
        
        # Create the haar cascade
        faceCascade1 = cv2.CascadeClassifier(cascPath1)
        faceCascade2 = cv2.CascadeClassifier(cascPath2)

        # initialize the camera and grab a reference to the raw camera capture
        camera = PiCamera()
        camera.resolution = (160, 120)
        camera.framerate = 32
        rawCapture = PiRGBArray(camera, size=(160, 120))

        # allow the camera to warmup
        time.sleep(0.1)
        lastTime = time.time()*1000.0


        for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
            print ("coe!")
            # capture frames from the camera until it gets a stop signal
            if (camera_stop.empty()):
                # grab the raw NumPy array representing the image, then initialize the timestamp
                # and occupied/unoccupied text
                image = frame.array
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                    
                # Detect frontal faces in the image
                faces1 = faceCascade1.detectMultiScale(
                gray,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(30, 30),
                flags = cv2.cv.CV_HAAR_SCALE_IMAGE
                )
                frontals=len(faces1)
                if (frontals>0):
                    print "Found {0} FRONTAL(S)!".format(frontals)
                    #lastTime = time.time()*1000.0

                # Detect profile faces in the image
                faces2 = faceCascade2.detectMultiScale(
                gray,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(30, 30),
                flags = cv2.cv.CV_HAAR_SCALE_IMAGE
                )
                profiles=len(faces2)
                if (profiles>0):
                    print "Found {0} PROFILE(S)!".format(profiles)
                    #lastTime = time.time()*1000.0

                rawCapture.truncate(0)
        
            # stop signal received
            else:
                camera_stop.get() #get the stop signal off the queue
                print("ta pra cabaaa")
                camera_stop.get() #block execution
                
    #terminate thread when keyboard interrupts occur
    except(KeyboardInterrupt, SystemExit):
        print("Wrapping camera thread up...")
        #rawCapture.truncate(0)
        sys.exit()
