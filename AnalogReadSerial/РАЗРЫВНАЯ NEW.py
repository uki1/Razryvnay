from Tkinter import *
import serial
import threading
import time

import csv


from time import gmtime, strftime


    
alls=[]
bv = 1
outA=0




class Application(Frame):
    def conec(self):
        global ser
        ser = serial.Serial("COM31")
        self.zna["text"] = "Connect"
        t.start()
        

    def conec2(self):
        global serP
        serP = serial.Serial(port='COM4', baudrate=250000)
        self.se2["text"] = "Connected"
        t2.start()
        
    def createWidgets(self):
        self.zna = Label(self)
        self.zna["text"] = "Disconnect"
        self.zna["fg"]   = "red"

        self.zna.pack({"side": "left"})

        self.zna2 = Label(self)
        self.zna2["text"] = "Disconnect"
        self.zna2["fg"]   = "red"

        self.hi_there = Button(self)
        self.hi_there["text"] = "Connect"
        self.hi_there["command"] = self.conec

        self.hi_there.pack({"side": "left"})

        self.se2 = Button(self)
        self.se2["text"] = "Connect 2"
        self.se2["command"] = self.conec2

        self.se2.pack({"side": "left"})
        
        self.seH = Button(self)
        self.seH["text"] = "HOME Z"
        self.seH["command"] = lambda: serP.write("G28 Z" + '\r\n')

        self.seH.pack({"side": "left"})

        self.se10 = Button(self)
        self.se10["text"] = "Z10",
        self.se10["command"] = lambda: serP.write("G1 Z100" + '\r\n')

        self.se10.pack({"side": "left"})
        self.zna2.pack({"side": "left"})
        
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
                writer.writerows([[al[0].split('.')[0],strftime("%H:%M:%S", gmtime()), zx.replace('.',','), outA]])
                
                app.zna["text"] = alls[-1][0]
                
                break
        
def clockP():
    global outA
    while 1 :
        serP.write("M114" + '\r\n')
        out = ''
        time.sleep(0.6)
        while serP.inWaiting() > 0:
            out += serP.read(1)
        if out != '':
            try:
                app.zna2["text"]=out
                outA = str(float(out.split('Count')[1].split('Z:')[1][:-4])).replace('.',',')
                app.zna2["text"]=outA
            except:
                pass
t = threading.Thread(target=clock, args=(15,))
t2 = threading.Thread(target=clockP)


app.mainloop()
bv=0
root.destroy()

