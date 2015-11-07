from Tkinter import *
import serial
import threading
import time

import csv


from time import gmtime, strftime


    
alls=[]
bv = 1
outA=0
outX=0
iu=7


class Application(Frame):
    def conec(self):
        global ser
        if self.con1:
            ser = serial.Serial("COM31")
            self.zna["text"] = "Connect"
            self.con1=0
            t.start()
        

    def conec2(self):
        global serP
        if self.con2:
            serP = serial.Serial(port='COM4', baudrate=250000)
            self.se2["text"] = "Connected"
            self.con2=0
            t2.start()
        
    def createWidgets(self):
        self.zna = Label(self)
        self.zna["text"] = "Disconnect"
        self.zna["fg"]   = "red"

        self.zna.grid(row = 1, column = 1)

        self.zna2 = Label(self)
        self.zna2["text"] = "Disconnect"
        self.zna2["fg"]   = "red"

        self.hi_there = Button(self)
        self.hi_there["text"] = "Connect"
        self.hi_there["command"] = self.conec

        self.hi_there.grid(row = 1, column = 2)

        self.se2 = Button(self)
        self.se2["text"] = "Connect 2"
        self.se2["command"] = self.conec2

        self.se2.grid(row = 1, column = 3)
        
        self.seH = Button(self)
        self.seH["text"] = "HOME Z"
        self.seH["command"] = lambda: serP.write("G28 Z" + '\r\n')

        self.seH.grid(row = 1, column = 4)

        self.se10 = Button(self)
        self.se10["text"] = "Z200"
        self.se10["command"] = lambda: serP.write("G1 Z200" + '\r\n')

        self.se11 = Button(self)
        self.se11["text"] = "F50"
        self.se11["command"] = lambda: serP.write("G1 F50" + '\r\n')
        
        self.se19 = Button(self)
        self.se19["text"] = "F1"
        self.se19["command"] = lambda: serP.write("G1 F1" + '\r\n')

        self.se12 = Entry(self)
        self.se15 = Label(self, text="LENGHT:")
        
        
        self.se13 = Entry(self)
        self.se16 = Label(self, text="DIAMETR:")
        

        self.se14 = Entry(self)
        self.se17 = Label(self, text="POLYMER:")

        self.canv = Canvas(self, width = 400, height = 400, bg = "white")
        self.canv.create_line(200,400,200,0,width=2,arrow=LAST) 
        self.canv.create_line(0,200,400,200,width=2,arrow=LAST) 



         
        
        self.se10.grid(row = 1, column = 5)
        self.se11.grid(row = 1, column = 6)
        self.se19.grid(row = 1, column = 7)
        self.se15.grid(row = 1, column = 8)
        self.se12.grid(row = 1, column = 9)
        self.se16.grid(row = 1, column = 10)
        self.se13.grid(row = 1, column = 11)
        self.se17.grid(row = 1, column = 12)
        self.se14.grid(row = 1, column = 13)
        self.zna2.grid(row = 1, column = 14)
        self.canv.grid(row = 2, column = 1, columnspan = 8)
        
        
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.con1=1
        self.con2=1
        self.pack()
        self.createWidgets()

root = Tk()
app = Application(master=root)


def clock(interval):
    writer = csv.writer(open("some "+ strftime("%d %b %H,%M,%S", gmtime()) +".csv", "wb"), delimiter=';', quoting=csv.QUOTE_MINIMAL, quotechar='`', lineterminator='\n')
    writer.writerows([['L0 = '+app.se12.get(),'d = ' + app.se13.get(), 'Polymer ' + app.se14.get()]])
    global outX
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

                if outX:
                    print "00000000"
                    if 'T:' in outX:
                        writer.writerows([[' ',' ', "TEMP:", outX]])
                        print "TEMP: " + outX
                    outX = 0
                    
                    
                print al
                alls.append(al)
                if (not outX) and (not iu):
                    writer.writerows([[al[0].split('.')[0],strftime("%H:%M:%S", gmtime()), zx.replace('.',','), outA]])
                    try:
                        float(zx)
                        writegraph(float(outA), float(zx))
                    except:
                        writegraph(float(outA.replace(',','.')), 0)
                app.zna["text"] = alls[-1][0]
                
                break
        
def clockP():
    global outA
    time.sleep(5)
    global iu
    global outX
    while iu :
        iu=iu-1
        serP.write("M105" + '\r\n')
        out = ''
        time.sleep(0.2)
        while serP.inWaiting() > 0:
            out += serP.read(1)
        if out != '':
            try:
                outX = str(out[:-4])
                print outX
            except:
                
                pass    
    
    while 1 :
        serP.write("M114" + '\r\n')
        out = ''
        time.sleep(0.2)
        while serP.inWaiting() > 0:
            out += serP.read(1)
        if out != '':
            try:
                app.zna2["text"]=out
                outA = str(float(out.split('Count')[1].split('Z:')[1][:-4])).replace('.',',')
                app.zna2["text"]=outA
            except:
                pass

def writegraph(x,y):
    x = int(x)*2
    y = int(y+50)/10
    app.canv.create_oval(x, y, x + 1, y + 1, fill = 'black')
    pass
            
t = threading.Thread(target=clock, args=(15,))
t2 = threading.Thread(target=clockP)


app.mainloop()
bv=0
root.destroy()

