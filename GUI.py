#!/usr/bin/python2.7
import sys
import os
from Tkinter import *
import tkMessageBox
top=Tk()

def helloCallBack():
    os.system('python mustache.py')

B=Button(top,text="Mustache Filter",command= helloCallBack)
B.pack()
top.geometry("200x200")
B.place(relx=0.5, rely=0.3, anchor="n")
l = Label(top, text = "CHOOSE A FILTER")
l.pack()

def helloCallBack():
    os.system('python glasses.py')

C=Button(top,text="Glasses Filter",command= helloCallBack)
C.pack()

C.place(relx=0.5, rely=0.5, anchor="n")


def helloCallBack():
    os.system('python redNose.py')

D=Button(top,text="Red Nose Filter",command= helloCallBack)
D.pack()

D.place(relx=0.5, rely=0.7, anchor="n")


#b2 = Tkinter.Button(top, text = "Avner filter")
#b3 = Tkinter.Button(top, text = "Other filter")

#b2.pack()
#b3.pack()


top.mainloop()
