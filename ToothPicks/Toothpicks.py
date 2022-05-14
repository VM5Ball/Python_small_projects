import tkinter as tk
import tkinter.ttk as ttk
from tkinter import ALL

#class Toothpick as the main object on the picture
class ToothPick:

    def __init__(self, info):
        self.info = info
        if (info[2] == -1):                             # if this toothpick is horizontal
            self.e1 = (info[0] - 20, info[1])           #x11 = x - 20, y11 = y
            self.e2 = (info[0] + 20, info[1])           #x12 = x + 20, y12 = y
        elif (info[2] == 1):                            # if this toothpick is vertical
            self.e1 = (info[0], info[1] - 20)           #x21 = x, y21 = y - 20
            self.e2 = (info[0], info[1] + 20)           #x22 = x, y22 = y + 20
    
    #function that returns an object of a toothpick (its x and y and orientation (info)) depending on its orientation
    def end1(self, otherPicks):
        for pick in otherPicks:
            if (pick.info != self.info):
                if (pick.e1 == self.e1 or self.e1 == pick.e2 or self.e1 == (pick.info[0], pick.info[1])):
                    return None
        return ToothPick((self.e1[0], self.e1[1], self.info[2]*(-1)))

    def end2(self, otherPicks):
        for pick in otherPicks:
            if (pick.info != self.info):
                if (pick.e1 == self.e2 or self.e2 == pick.e2 or self.e2 == (pick.info[0], pick.info[1])):
                    return None
        return ToothPick((self.e2[0], self.e2[1], self.info[2]*(-1)))




toothPicks = []               #list of all toothpicks together
activeToothPics = []          #list of toothpick that are active on the current step
prevActiveToothPicks = []     #list that contains toothpick on the previous step so we can decrease and increase its value

class mainMenu:
    
    def __init__(self, master):
        self.master = master                     #window that this object refers to
        self.master.geometry('800x600')
        self.frame = tk.Frame(self.master)      #frame is a place for widgets, frame is located in the main window (master)
        self.frame.pack()
        self.prevGeneration = 0                   #version of the picture (scalebar)
        self.drawPicksCanvas = tk.Canvas(self.frame, width = 600, height = 600)
        self.drawPicksCanvas.grid(rowspan = 3, column = 0)
        self.spinBoxValue = tk.IntVar()                          #value that spinbox contains
        self.spinBoxValue.set(0)                             #set default value for the spinbox 0 
        self.spinBox = ttk.Spinbox(self.frame, from_ = 1, to = 10000, textvariable = self.spinBoxValue, command = self.updatePicks, state = 'readonly', width = 4)
        self.spinBox.grid(row = 1, column = 1, sticky = 'n') 
        self.scaleBar = tk.Scale(self.frame, from_ = 100, to = 1, orient = 'horizontal', command = lambda x: self.scale(self.scaleBar.get()*0.01), length = 100)
        self.scaleBar.set(100)
        self.scaleBar.grid(row = 1, column = 1, sticky = 's')
  
    #function that scales the canvas
    def scale(self, scaleAmount):
        self.drawPicks()
        self.drawPicksCanvas.scale(ALL, 300, 300, scaleAmount, scaleAmount)
        
    def updatePicks(self):
        self.updatedGeneration = int(self.spinBox.get())                #get the number that is in the scale box to calculate how many toothpic should br in the frame
        if (self.updatedGeneration > self.prevGeneration):              #case when we increase the step
            if (self.updatedGeneration == 1 and activeToothPics == []):    #case of the first drawing
                prevActiveToothPicks.clear()
                activeToothPics.append(ToothPick((600/2, 600/2, 1)))      #we append one main toothpick to the list of active toothpicks that are on the frame
                prevActiveToothPicks.append(activeToothPics)              #we append the whole list of active toothpics to the list of previous toothpics for the next step
            else:
                tempPicks = []
                toothPicks.extend(activeToothPics)
                temp = activeToothPics.copy()
                prevActiveToothPicks.append(temp)
                for pick in activeToothPics:                           #for every toothpick we are going to ckeck its ends
                    if (pick.end1(toothPicks) != None):
                        tempPicks.append(pick.end1(toothPicks))
                    if (pick.end2(toothPicks) != None):
                        tempPicks.append(pick.end2(toothPicks))
                activeToothPics.clear()
                activeToothPics.extend(tempPicks)                     #we add temporary picks to the list of active toothpicks
                self.prevGeneration = self.updatedGeneration          #we update previous generation

        elif (self.updatedGeneration < self.prevGeneration):           #case where we decrease the amount od toothpicks
            tempPicks = [i for i in toothPicks if i not in activeToothPics]
            toothPicks.clear()
            toothPicks.extend(tempPicks)
            activeToothPics.clear()            
            activeToothPics.extend(prevActiveToothPicks[prevActiveToothPicks.__len__()-1])
            prevActiveToothPicks.pop()
        self.prevGeneration = self.updatedGeneration
        self.scale(self.scaleBar.get()*0.01)       #with the gelp of scale function we draw new toothpicks

    #function that draws toothpick
    def drawPicks(self):
        self.drawPicksCanvas.delete('all')
        #existing toothpicks
        for pick in toothPicks:
            self.drawPicksCanvas.create_line(pick.e1[0], pick.e1[1], pick.e2[0], pick.e2[1], width = 2)
        #new toothpicks that appeared on this step
        for pick in activeToothPics:                                                                     
            self.drawPicksCanvas.create_line(pick.e1[0], pick.e1[1], pick.e2[0], pick.e2[1], fill = 'blue', width = 2)

def main():    
    root = tk.Tk(className = 'ToothPicks')
    root.title('ToothPicks')
    root.resizable(False, False)
    app = mainMenu(root)
    root.mainloop()

if __name__ == '__main__':
    main()