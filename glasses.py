# Project: Live Webcam Video Filters
# Contributers: Abraham Medina, Gurjot Sandhu, Valentina Fuchs Facht
# Class: CST 205-02 Spring 2017
# Date: March 16, 2017
# Abstract: This program allows the user to activate the webcam of a computer according to a filter they would like put over their face and to be able to then take a photo with the given filter
# Contribution: Abraham and Valentina worked on getting the primary mustache code working then Valentina split off to do the glasses filter while Abraham continued to refine the primary code. Gurjot worked on the GUI and also worked with Abraham to find most of the resources used in the project. Gurjot also worked on the main implementation of the red nose filter.
# Github: https://github.com/abrahamleyva/Project3Team248

import cv2
import sys
import time
from pygame import mixer

# Loading and playing the timer sound
mixer.init()
mixer.music.load('sounds/sound.mp3')

# building necessary cv2 Cascade files
faceCascade = cv2.CascadeClassifier("hars/face.xml")
eyesCascade = cv2.CascadeClassifier("hars/haarcascade_mcs_eyepair_small.xml")

# Loads our image with only the non-transparent sections visible
imgGlasses = cv2.imread('filters/glasses.png', -1)

# Create the mask for the filter based on the visible parts of the image
orig_mask = imgGlasses[:, :, 3]

# Create the mask for the area surrounding our orig_mask
orig_mask_inv = cv2.bitwise_not(orig_mask)

# Convert glasses image to BGR and save the original image size
imgGlasses = imgGlasses[:, :, 0:3]
origGlassesHeight, origGlassesWidth = imgGlasses.shape[:2]

# get video feed from primary system webcam
video_capture = cv2.VideoCapture(0)

# starts playing timer sound
mixer.music.play()

# starts the 17 second loop
while time.clock() < 17:

    # Capture video feed
    ret, frame = video_capture.read()

    # Create greyscale image from the video feed so hars can read the feed
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in input video stream
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE
    )

    # Iterate over each face found in the webcam
    for (x, y, w, h) in faces:
        
        # Creats a gray scale and colored version of the area of the face for the hars
        roi_gray = gray[y:y + h, x:x + w]
        roi_color = frame[y:y + h, x:x + w]

        # Detect all eyess found within the face area
        eyes = eyesCascade.detectMultiScale(roi_gray)

        for (ex, ey, ew, eh) in eyes:
            
            # Resizes the size of the image with respect to the eyes found
            glassesWidth = 3 * ew
            glassesHeight = glassesWidth * origGlassesHeight / origGlassesWidth

            # Center the glasses on the bottom of the eyes
            x1 = ex - (glassesWidth / 2)
            x2 = ex + ew + (glassesWidth / 2)
            y1 = ey + eh - (glassesHeight / 4)
            y2 = ey + eh + (glassesHeight / 4)
            
            # Prevents the glasses from going outside of the face boundry
            if x1 < 0:
                x1 = 0
            if y1 < 0:
                y1 = 0
            if x2 > w:
                x2 = w
            if y2 > h:
                y2 = h

			# Re-re-calculate the width and height of the glasses image
            glassesWidth = x2 - x1
            glassesHeight = y2 - y1

            # Re-size the original image and the masks to the glasses sizes
            # calcualted above
            glasses = cv2.resize(imgGlasses, (glassesWidth, glassesHeight), interpolation=cv2.INTER_AREA)
            mask = cv2.resize(orig_mask, (glassesWidth, glassesHeight), interpolation=cv2.INTER_AREA)
            mask_inv = cv2.resize(orig_mask_inv, (glassesWidth, glassesHeight), interpolation=cv2.INTER_AREA)

            # equals the ROI image size to the resized BGR image
            roi = roi_color[y1:y2, x1:x2]

            # finds which pixles the image should not be in
            roi_bg = cv2.bitwise_and(roi, roi, mask=mask_inv)

            # Selects the pixles form the BGR image that should be present
            roi_fg = cv2.bitwise_and(glasses, glasses, mask=mask)

            # joins the last two images without any overlap
            dst = cv2.add(roi_bg, roi_fg)

            # place the final image filter over the feed
            roi_color[y1:y2, x1:x2] = dst

			# breaks out of the loop before multiple eyess are found in on one face
            break

    # Takes a frame image of the frame
    cv2.imwrite('image.jpg', frame)
    
    # Display the resulting frame
    cv2.imshow('Video', frame)

    # Press any key to exit or wait for timer to finish
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()
