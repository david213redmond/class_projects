#!/usr/bin/env python
from tkinter import*
from final import*

radius = 2
isRed = TRUE
data_pos = []
data_neg = []
def process():
    global canvas
    global radius
    f = open("coordinates.txt",'w')
    for xy in data_pos:
        f.write(str(xy[0])+' '+str(xy[1])+' --> 0\n')
    for xy in data_neg:
        f.write(str(xy[0])+' '+str(xy[1])+' --> 1\n')
    f.close()
    svm_main(data_pos, data_neg)
##    h = hyperplane()
##    for xy in h:
##        canvas.create_oval(xy[0]-radius,xy[1]-radius,xy[0]+radius,xy[1]+radius, fill='black')

def click(event):
    global radius
    global isRed
    global data
    if isRed:
        canvas.create_oval(event.x-radius, event.y-radius,event.x+radius, event.y+radius, fill='red')
        isRed = FALSE
        data_pos.append([event.x,event.y])
    else:
        canvas.create_oval(event.x-radius, event.y-radius,event.x+radius, event.y+radius, fill='blue')
        isRed = TRUE
        data_neg.append([event.x,event.y])
    
root = Tk()


button_1 = Button(root,text = "Done", font=('Sims',12), command = process)
button_2 = Button(root,text = "Quit", font=('Sims',12), command = root.destroy)

canvas = Canvas(root, width=1000, height=400)
canvas.grid(column=0, row=0, sticky=('N', 'W', 'E', 'S'))
canvas.bind("<Button-1>", click)
button_2.pack()
button_1.pack()
canvas.pack()

root.mainloop()
