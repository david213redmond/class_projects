#ImageSeg.py
##fields
from tkinter import*
import math
width = 4   #the width of the pixel matrix.
height = 3  #the height of the pixel matrix.
ntrees = 2  #the amount of trees produced by the kruskal algorithm before stopping.
totalPixels = [[(50, 50, 50), (50, 50, 50), (50, 50, 50), (79, 20, 16)],    #a sample pixel matrix
 [(32, 93, 78), (50, 50, 50), (78, 21, 17), (79, 20, 16)],
 [(31, 89, 78), (33, 90, 77), (79, 21, 15), (77, 20, 17)]]
hedges = [] #list that stores the horizontal edges
vedges = [] #list that stores the vertical edges
upTrees = []    #an uptree array implementation for the disconnected trees.

##the object that contains the information about the edges.
class Edge:
    def __init__(self, i, w):
        self.index = i
        self.weight = w
    def __repr__(self):
        return repr((self.index,self.weight))

##getting the euclidean distance between two pixels' RGB values
def getD(p1,p2):
    return math.sqrt(pow(p1[0]-p2[0],2)+pow(p1[1]-p2[1],2)+pow(p1[2]-p2[2],2))

##union and find use the index of the vertex as its identity.
def find(v):
    index = v
    while upTrees[index] != -1:
        index = upTrees[index]
    return index
def union(v1,v2):
    i1 = find(v1)
    i2 = find(v2)
    upTrees[i1] = i2

##graphPoints and graphEdge are the methods I used along with tkinter to implement a graphical representation of the result of trees.
def graphPoint(i):
    global canvas
    canvas.create_oval(100+(i%width)*800/width-1,100+(i//width)*800/width-1,100+(i%width)*800/width+1,100+(i//width)*800/width+1)
def graphEdge(i,j):
    global canvas
    canvas.create_line(100+(i%width)*800/width,100+(i//width)*800/width,100+(j%width)*800/width,100+(j//width)*800/width)   
            
        
##The main kruskal algorithm.
##given the pixel matrix, kruskal will print the segmented values for each corresponding pixel.
def kruskal(pixels):
    for i in range(0,height):
        for j in range(0,width-1):
            ##build the hedges.
            p1 = pixels[i][j]
            p2 = pixels[i][j+1]
            w_h = getD(p1,p2)
            e_h = Edge(i*(width-1)+j,w_h)
            hedges.append(e_h)
    for i in range(0,height-1):
        for j in range(0,width):
            ##build the vedges.
            p1 = pixels[i][j]
            p2 = pixels[i+1][j]
            w_v = getD(p1,p2)
            e_v = Edge(i*width+j,w_v)
            vedges.append(e_v)
    hedges.sort(key=lambda e: e.weight,reverse=True)
    vedges.sort(key=lambda e: e.weight,reverse=True)
    ##Kruskal
    ##pixels p(0) ~ p(N-1)
    ##We have a total of N vertices.
    N = width*height
    count = N - ntrees
    for i in range(0,N):
        upTrees.append(-1)
    while len(vedges)+len(hedges) > 0:
        if count == 0:
            break
        u = 0
        v = 0
        e = 0
        hOrV = 'h'
        index = 0
        if len(vedges) == 0 or hedges[-1].weight <= vedges[-1].weight:
            index = hedges[-1].index
            u = index+index//(width-1)
            v = index+index//(width-1) + 1
            e = hedges.pop()
        elif len(hedges) == 0 or hedges[-1].weight > vedges[-1].weight:
            index = vedges[-1].index
            u = index
            v = index + width
            e = vedges.pop()
            hOrV = 'v'
        if find(u) != find(v):
            count -= 1
            union(u,v)
            graphEdge(u,v)
    for i in range(0,N):
        graphPoint(i)
    ##print the outputs
    output = []
    roots = []
    for i in range(0,height):
        row = []
        for j in range(0,width):
            v = j + i*width
            root = find(v)
            if root in roots:
                index = roots.index(root)
            else:
                roots.append(root)
                index = len(roots)-1
            row.append(index)
        output.append(row)
    print(output)
##main
##using tkinter to do a graphical representation.
root = Tk()
canvas = Canvas(root, width=1000, height = 1000)
canvas.create_text(500,50,text='ntrees = '+str(ntrees)+' representation')
canvas.pack()
totalPixels = []
##updating the pixel matrix, height, and width to that of earth-sm2.txt.
f = open('earth-sm2.txt','r')
totalPixels = eval(f.read())
height = len(totalPixels)
width = len(totalPixels[0])
kruskal(totalPixels)
root.mainloop()
