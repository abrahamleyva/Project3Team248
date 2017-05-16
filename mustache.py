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
noseCascade = cv2.CascadeClassifier("hars/nose.xml")

# Loads our image with only the non-transparent sections visible
imgMustache = cv2.imread('filters/mustache.png', -1)

# Create the mask for the filter based on the visible parts of the image
orig_mask = imgMustache[:, :, 3]

# Create the mask for the area surrounding our orig_mask
orig_mask_inv = cv2.bitwise_not(orig_mask)

# Convert mustache image to BGR and save the original image size
imgMustache = imgMustache[:, :, 0:3]
origMustacheHeight, origMustacheWidth = imgMustache.shape[:2]

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

        # Detect all noses found within the face area
		nose = noseCascade.detectMultiScale(roi_gray)

		for (nx, ny, nw, nh) in nose:

            # Resizes the size of the image with respect to the nose found
			mustacheWidth = 3 * nw
			mustacheHeight = mustacheWidth * origMustacheHeight / origMustacheWidth

            # Center the mustache on the bottom of the nose
			x1 = nx - (mustacheWidth / 4)
			x2 = nx + nw + (mustacheWidth / 4)
			y1 = ny + nh - (mustacheHeight / 2)
			y2 = ny + nh + (mustacheHeight / 2)

            # Prevents the mustache from going outside of the face boundry
			if x1 < 0:
				x1 = 0
			if y1 < 0:
				y1 = 0
			if x2 > w:
				x2 = w
			if y2 > h:
				y2 = h

            # Re-re-calculate the width and height of the mustache image
			mustacheWidth = x2 - x1
			mustacheHeight = y2 - y1

            # Re-size the original colored image and the masks to the mustache sizes
            # calcualted above
			mustache = cv2.resize(imgMustache, (mustacheWidth, mustacheHeight), interpolation=cv2.INTER_AREA)
			mask = cv2.resize(orig_mask, (mustacheWidth, mustacheHeight), interpolation=cv2.INTER_AREA)
			mask_inv = cv2.resize(orig_mask_inv, (mustacheWidth, mustacheHeight), interpolation=cv2.INTER_AREA)

            # equals the ROI image size to the resized BGR image
			roi = roi_color[y1:y2, x1:x2]

            # finds which pixles the image should not be in
			roi_bg = cv2.bitwise_and(roi, roi, mask=mask_inv)

            # Selects the pixles form the BGR image that should be present
			roi_fg = cv2.bitwise_and(mustache, mustache, mask=mask)

            # joins the last two images without any overlap
			dst = cv2.add(roi_bg, roi_fg)

            # place the final image filter over the feed
			roi_color[y1:y2, x1:x2] = dst
			
			# breaks out of the loop before multiple noses are found in on one face
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
