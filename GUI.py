#!/usr/bin/python2.7
import sys
import os
import Tkinter
import tkMessageBox
top=Tkinter.Tk()

def helloCallBack():
    os.system('python test.py')

B=Tkinter.Button(top,text="Start Camera",command= helloCallBack)
B.pack()
top.geometry("200x100")
B.place(relx=0.5, rely=0.5, anchor="center")
top.mainloop()
