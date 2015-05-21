from Tkinter import *
from FINAL_SRL import *
from featureExtraction_Propbank_final_stanford import Feature
import tkMessageBox


root = Tk()
root.geometry("500x200")
frame = Frame(root)
frame.pack()

midframe = Frame(root)
midframe.pack()

bottomframe = Frame(root)
bottomframe.pack()

L1 = Label(frame,font=20, text="Enter Sentence : ")
L1.pack( side = LEFT)
E1 = Entry(frame,width=50, bd =1)
E1.pack(side = LEFT)

L2 = Label(midframe,font=20, text="Predicate position : ")
L2.pack( side = LEFT)
E2 = Entry(midframe,width=50, bd =1)
E2.pack(side = LEFT)



def helloCallBack1():
   # tkMessageBox.showinfo( "Hello Python", "Hello World")
   FINAL()

def helloCallBack2():
   # tkMessageBox.showinfo( "Hello Python", "Hello World")
   text=E1.get()
   index=E2.get()
   query(text,index)

B = Button(bottomframe, text =" TRAIN SVM ", command = helloCallBack1)
B.pack()

B2 = Button(bottomframe, text ="Label the Sentence", command = helloCallBack2)
B2.pack()

root.mainloop()