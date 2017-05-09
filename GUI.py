#!/usr/bin/python2.7
import sys
import os
from Tkinter import *
import tkMessageBox
top=Tk()
top.wm_title("       Filters")
photo = PhotoImage(file = "sponge.gif")
label2 = Label(image=photo)
label2.image = photo
l = Label(top, text = "CHOOSE A FILTER", fg = 'black')
l.pack()
label2.pack()
def helloCallBack():
    os.system('python mustache.py')

B=Button(top,text="Mustache Filter", fg = 'blue',command= helloCallBack)
B.pack()
top.geometry("450x270")
B.place(relx=0.247, rely=0.478, anchor="n")

def helloCallBack():
    os.system('python glasses.py')

C=Button(top,text="Glasses Filter", fg = 'green',command= helloCallBack)
C.pack()

C.place(relx=0.269, rely=0.60, anchor="n")


def helloCallBack():
    os.system('python redNose.py')

D=Button(top,text="Red Nose Filter", fg = 'red',command= helloCallBack)
D.pack()

D.place(relx=0.26, rely=0.72, anchor="n")


#b2 = Tkinter.Button(top, text = "Avner filter")
#b3 = Tkinter.Button(top, text = "Other filter")

#b2.pack()
#b3.pack()


top.mainloop()
