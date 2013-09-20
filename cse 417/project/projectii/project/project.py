import math

class Pixel:
	row = 0
	column = 0
	rgb = []
	edges = []
	bkEdges = []
	 
	def __init__(self, c, r, rgbColors):
		self.row = r 
		self.column = c
		self.rgb = rgbColors
		self.edges = []
		self.bkEdges = []
	
	def addEdge(self, edge):
		self.edges.append(edge)

	def getRed(self):
		return self.rgb[0]

	def getGreen(self):
		 return self.rgb[1]

	def getBlue(self):
		return self.rgb[2]	
	def __str__(self):
		return "(" + str(self.row) + ", " + str(self.column) + ") with RGB:" + str(self.rgb)

class Edge:
	p1 = Pixel
	p2 = Pixel
	capacity = 0
	forwardEdge = 0
	backwardEdge = 0
	flow = 0

	def __init__(self, pixel1, pixel2, cap):
		self.p1 = pixel1
		self.p2 = pixel2
		self.capacity = cap
		self.forwardEdge = cap
		self.backwardEdge = 0
		self.flow = 0
	 
	def __str__(self):
		return "[" + str(self.p1) + " - " + str(self.p2) + "] | Flow:" + str(self.flow) 


'MAIN PROGRAM'

ED = []
EDO = []
'location to image'
PATH = 'D:\\project\\ladyliberty\\ll1.jpg'

pmOpenImage(1, PATH)

'Matrix of the image in PATH as a nested list of rows of pixels inside'
'a list for the whole image. Pixels in the rows are further represented'
'as a list of three values, the rgb value of a pixel.'
h = pmGetImageHeight(1)
w = pmGetImageWidth(1)

pixels = []
source = Pixel(0, 0, [])

for i in range(h):
	for j in range(w):
		pixels.append(Pixel(i, j, [ pmGetPixel(1, j, i)[0], pmGetPixel(1, j, i)[1], pmGetPixel(1, j, i)[2] ] ))


'edges connecting the source node to each pixel [i.e. the chance that the given pixel is part of Statue of Liberty]'
'and the edges connecting each pixel to the sink [i.e. the chance that the given pixel is not part of ll]'
for i in range(len(pixels)):
	ed = math.sqrt((pixels[i].getRed() - 87)**2 + (pixels[i].getGreen() - 120)**2 + (pixels[i].getBlue() - 118)**2)
	 
	'-1 is source; -2 is sink'
	s_i = Edge(-1, pixels[i], 200-int(ed))
	i_t = Edge(pixels[i], -2, int(ed)+50)

	ED.append(s_i)
	pixels[i].edges.append(i_t)
	EDO.append(i_t)


'Create all the neighboring LEFT edges as edges[2]'
for i in range(len(pixels)):
	if(i % w != 0):
		euclidian = math.sqrt( (pixels[i].getRed() - pixels[i-1].getRed()) ** 2 + (pixels[i].getGreen() - pixels[i-1].getGreen()) ** 2 + (pixels[i].getBlue() - pixels[i-1].getBlue()) ** 2 ) 
		pixels[i].addEdge(Edge(pixels[i], pixels[i-1], 255-int(euclidian)))
		pixels[i-1].bkEdges.append( Edge( pixels[i-1], pixels[i], 255-int(euclidian) ) )


'Create all the neighboring RIGHT edges as edges[3]'
for i in range(len(pixels)):
	if(i % w != w-1):
		euclidian = math.sqrt( (pixels[i].getRed() - pixels[i+1].getRed()) ** 2 + (pixels[i].getGreen() - pixels[i+1].getGreen()) ** 2 + (pixels[i].getBlue() - pixels[i+1].getBlue()) ** 2 ) 
		pixels[i].addEdge(Edge(pixels[i], pixels[i+1], 255-int(euclidian)))
		pixels[i+1].bkEdges.append( Edge( pixels[i+1], pixels[i], 255-int(euclidian)) )

'Create all the neighboring UP edges as edges[4]'
for i in range(len(pixels)-w):
	euclidian = math.sqrt( (pixels[i].getRed() - pixels[i+w].getRed()) ** 2 + (pixels[i].getGreen() - pixels[i+w].getGreen()) ** 2 + (pixels[i].getBlue() - pixels[i+w].getBlue()) ** 2 ) 
	pixels[i].addEdge(Edge(pixels[i], pixels[i+w], 255-int(euclidian)))
	pixels[i-w].bkEdges.append( Edge( pixels[i+w], pixels[i], 255-int(euclidian)) )

	 
'Create all the neighboring DOWN edges as edges[5]'
for i in range(w, len(pixels)):
	euclidian = math.sqrt( (pixels[i].getRed() - pixels[i-w].getRed()) ** 2 + (pixels[i].getGreen() - pixels[i-w].getGreen()) ** 2 + (pixels[i].getBlue() - pixels[i-w].getBlue()) ** 2 ) 
	pixels[i].addEdge(Edge(pixels[i], pixels[i-w], 255-int(euclidian)))
	pixels[i-w].bkEdges.append( Edge( pixels[i-w], pixels[i], 255-int(euclidian)) )

pixelsVisited = []
def getPath(edge, delta, path):
	if edge.forwardEdge < delta:
		return None
	pixelsVisited.append(edge.p1)

	if edge.p2 == -2:
		return path
	for e in edge.p2.edges:
		if e.forwardEdge > delta and not (e.p2 in pixelsVisited):
			result = getPath(e, delta, path + [e])
			if result != None:
				return result
#	for e in edge.p2.bkEdges:
#		if e.backwardEdge > delta and not (e in path):
#			result = getPath(e, delta, path + e)
#			if result != None:
#				return Result

#for edge in ED:
#	path = getPath(edge, 128, [edge])
#	if path != None:
#		for e in path:
#			print(str(e) + "   -   "),
#			print()
#	else:
#		print("No path")
#
#	print
#	print


#for edge in ED:
#	print(str(edge))


def getP(delta):
	for edge in ED:
		path = getPath(edge, delta, [edge])
		if path != None:
			return path

def augment(path):
	bottleneck = 255
	for edge in path:
		if edge.forwardEdge < bottleneck:
			bottleneck = edge.forwardEdge

	for edge in path:
		if edge.p1 == -1:
			edge.flow = edge.flow + bottleneck
			edge.forwardEdge = edge.forwardEdge - bottleneck
		elif edge in edge.p1.edges:
			edge.flow = edge.flow + bottleneck
			edge.forwardEdge = edge.forwardEdge - bottleneck
		#elif edge in edge.p1.bkEdges:
		#	edge.flow = edge.flow - bottleneck
			
			

delta = 0
for pixel in pixels:
	if pixel.edges[0].capacity > delta:
		delta = pixel.edges[0].capacity
delta = ( 2**int(math.log(delta, 2)))

while delta >= 1:

	path = getP(delta)
	loops = 0

	while path != None:
		augment(path)
		path = getP(delta)
		


		loops = loops+1
	delta = delta / 2

	print(delta)



print('fin')
print



print("Everywhere I can get to from E[0]:")

visited = []
def getCut(e, node):
	if e.forwardEdge > 0:
		visited.append(node)
		for edge in node.edges:
			if edge.forwardEdge > 128 and not node in visited:
				print(str(edge))
				getCut(edge.p2)


for edge in ED:
	getCut(edge, edge.p2)


for pix in visited:
	x = pix.column
	y = pix.row
	pmSetFormula("if{x =" + str(x) + " and y = " + str(y) + "} then RGB(0, 0, 0) Else RGB(Red1(x, y), Green1(x,y), Blue1(x, y))")
	pmCompute()
	
	print(str(pix))