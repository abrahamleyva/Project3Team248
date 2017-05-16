# Project: Live Webcam Video Filters
# Contributers: Abraham Medina, Gurjot Sandhu, Valentina Fuchs Facht
# Class: CST 205-02 Spring 2017
# Date: March 16, 2017
# Abstract: This program allows the user to activate the webcam of a computer according to a filter they would like put over their face and to be able to then take a photo with the given filter
# Contribution: Abraham and Valentina worked on getting the primary mustache code working then Valentina split off to do the glasses filter while Abraham continued to refine the primary code. Gurjot worked on the GUI and also worked with Abraham to find most of the resources used in the project. Gurjot also worked on the main implementation of the red nose filter.
# Github: https://github.com/abrahamleyva/Project3Team248

#!/usr/bin/python2.7
import sys
import os
from Tkinter import *
import tkMessageBox
top=Tk()
#changes the GUI's title to Filters
top.wm_title("       Filters")
#Bringing in our spongebob photo				
photo = PhotoImage(file = "sponge.gif")
#settign that photo as a label
label2 = Label(image=photo)
label2.image = photo
#Printing Choose a Filter at the top of the GUI
l = Label(top, text = "CHOOSE A FILTER", fg = 'black')
l.pack()
label2.pack()
#Command allows us to use the buttons to start our programs
def helloCallBack():
    os.system('python mustache.py')	#Puting this code into this button
#Labeling the Button as Mustache FIlter and changing the color of the text to blue
B=Button(top,text="Mustache Filter", fg = 'blue',command= helloCallBack)
B.pack()
#Size of the GUI window
top.geometry("450x270")
#Location where the Button will be placed in the GUI window
B.place(relx=0.247, rely=0.478, anchor="n")
#Command allows us to use the buttons to start our programs
def helloCallBack():
    os.system('python glasses.py') #Associating this code with this button
#Labeling button as Glasses Filter and changing text color to green
C=Button(top,text="Glasses Filter", fg = 'green',command= helloCallBack)
C.pack()
#Location where the Button will be placed in the GUI window
C.place(relx=0.269, rely=0.60, anchor="n")
#Labeling the Button as Mustache FIlter and changing the color of the text to blue
def helloCallBack():
    os.system('python redNose.py')	#Associating this code with this button
#Labeling button as Red Nose Filter and changing text color to red
D=Button(top,text="Red Nose Filter", fg = 'red',command= helloCallBack)
D.pack()
#Location where the Button will be placed in the GUI window
D.place(relx=0.26, rely=0.72, anchor="n")
top.mainloop()
