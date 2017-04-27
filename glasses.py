import cv2  # OpenCV Library
import sys
import time
from pygame import mixer
 
#-----------------------------------------------------------------------------
#       Load and configure Haar Cascade Classifiers
#-----------------------------------------------------------------------------
 
# build our cv2 Cascade Classifiers
faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
noseCascade = cv2.CascadeClassifier("haarcascade_mcs_nose.xml")
eye_cascade = cv2.CascadeClassifier("haarcascade_eye.xml")
 
#-----------------------------------------------------------------------------
#       Load and configure glasses (.png with alpha transparency)
#-----------------------------------------------------------------------------
 
# Load our overlay image: glasses.png
imgGlasses = cv2.imread('glasses.png',-1)
 
# Create the mask for the glasses
orig_mask = imgGlasses[:,:,3]
 
# Create the inverted mask for the glasses
orig_mask_inv = cv2.bitwise_not(orig_mask)
 
# Convert glasses image to BGR
# and save the original image size (used later when re-sizing the image)
img = imgGlasses[:,:,0:3]
origGlassesHeight, origGlassesWidth = imgGlasses.shape[:2]
 
#-----------------------------------------------------------------------------
#       Main program loop
#-----------------------------------------------------------------------------
 
# collect video input from first webcam on system
video_capture = cv2.VideoCapture(0)
 
while True:
    # Capture video feed
    ret, frame = video_capture.read()
 
    # Create greyscale image from the video feed
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
 
    # Detect faces in input video stream
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv2.cv.CV_HAAR_SCALE_IMAGE
    )
 
   # Iterate over each face found
    for (x, y, w, h) in faces:
        # Un-comment the next line for debug (draw box around all faces)
        # face = cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
 
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]
 
        # Detect eyes within the region bounded by each face (the ROI)
        eyes = eye_cascade.detectMultiScale(roi_gray)
 
        for(ex, ey, ew, eh) in eyes:
        #cv2.rectangle(roi_color,(ex,ey), (ex+ew, ey+eh), (0,255,0),2)
    
            roi_gray = gray[ey:ey+eh, ex:ex+ew]
            roi_color = img[ey:ey+eh, ex:ex+ew]
        
        # The glasses should be three times the width of the eyes
            glassesWidth =  2 * ew
            glassesHeight = glassesWidth * origGlassesHeight / origGlassesWidth
 
            # Center the glasses on top of eyes
            e1 = ex - (glassesWidth/4)
            e2 = ex + ew + (glassesWidth/4)
            e1 = ey + eh - (glassesHeight/2)
            e2 = ey + eh + (glassesHeight/2)
 
            # Check for clipping
            if e1 < 0:
                e1 = 0
            if e1 < 0:
                e1 = 0
            if e2 > w:
                e2 = w
            if e2 > h:
                e2 = h
 
            # Re-calculate the width and height of the glasses image
            glassesWidth = e2 - e1
            glassesHeight = e2 - e1
 
            # Re-size the original image and the masks to the glasses sizes
            # calcualted above
            glasses = cv2.resize(imgGlasses, (glassesWidth,glassesHeight), interpolation = cv2.INTER_AREA)
            mask = cv2.resize(orig_mask, (glassesWidth,glassesHeight), interpolation = cv2.INTER_AREA)
            mask_inv = cv2.resize(orig_mask_inv, (glassesWidth,glassesHeight), interpolation = cv2.INTER_AREA)
 
            # take ROI for glasses from background equal to size of glasses image
            roi = roi_color[e1:e2, e1:e2]
 
            # roi_bg contains the original image only where the glasses is not
            # in the region that is the size of the glasses.
            roi_bg = cv2.bitwise_and(roi,roi,mask = mask_inv)
 
            # roi_fg contains the image of the glasses only where the glasses is
            roi_fg = cv2.bitwise_and(glasses,glasses,mask = mask)
 
            # join the roi_bg and roi_fg
            dst = cv2.add(roi_bg,roi_fg)
 
            # place the joined image, saved to dst back over the original image
            roi_color[e1:e2, e1:e2] = dst
 
            break
 
    # Display the resulting frame
    cv2.imshow('Video', frame)
 
    # press any key to exit
    # NOTE;  x86 systems may need to remove: &amp;amp;amp;amp;amp;amp;amp;quot;&amp;amp;amp;amp;amp;amp;amp;amp; 0xFF == ord('q')&amp;amp;amp;amp;amp;amp;amp;quot;
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
 
# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()
