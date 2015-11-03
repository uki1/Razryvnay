from Tkinter import *
import serial
import threading
import time

import csv


from time import gmtime, strftime


    
alls=[]
bv = 1
class Application(Frame):
    def conec(self):
        global ser
        ser = serial.Serial("COM31")
        self.zna["text"] = "Connect"
        t.start()

        
    def createWidgets(self):
        self.zna = Label(self)
        self.zna["text"] = "Disconnect"
        self.zna["fg"]   = "red"

        self.zna.pack({"side": "left"})

        self.hi_there = Button(self)
        self.hi_there["text"] = "Connect",
        self.hi_there["command"] = self.conec

        self.hi_there.pack({"side": "left"})

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()

root = Tk()
app = Application(master=root)


def clock(interval):
    writer = csv.writer(open("some "+ strftime("%d %b %H,%M,%S", gmtime()) +".csv", "wb"), delimiter=';', quoting=csv.QUOTE_MINIMAL, quotechar='`', lineterminator='\n')
    while bv:
        al=[]
        for i in range(9):
            x = ser.readline()
            x = x.split(";")
            try:
                x[1]=x[1][:-2]
            except:
                break
            al.append(x)
            if "-" in x[1]:
                zx=x[0]
                al = al[:-1]
                x = 0
                for i in al:
                    try:
                        i[1]=float(i[1])
                    except:
                        i[1]=-1
                for i in al:
                    if i[1]>x: x=i[1]
                
                for i in al:
                    if i[1]==x: al = i

                print al
                alls.append(al)
                writer.writerows([[al[0].split('.')[0],strftime("%H:%M:%S", gmtime()), zx]])
                
                app.zna["text"] = alls[-1][0]
                
                break
        

        
t = threading.Thread(target=clock, args=(15,))


app.mainloop()
bv=0
root.destroy()

