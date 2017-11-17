import pyglet
from pyglet import graphics as gfx

from numpy.random import random as rnd

# from other.log import RiseLogLevel, LogIt as Log


# HowTo:
# 1. Create
# 2. Place
# 3. Draw

class Color:
	def CreateColorDict(self):
		colorDict = {
			"white" : [255, 255, 255]
			}
		return colorDict
		
	def RndColVal(self):
		return int(rnd()*256)
		
	def RandomColor(self, nodeNum):
			# Log("Generating random node colors...", 3)
			ret = []
			for i in range(nodeNum):
				ret += [[self.RndColVal(), self.RndColVal(), self.RndColVal()]]
			return ret
		
		
		
class ColSquare(Color):
	def __init__(self):
		# Log("A square has been created!", 2)
		self.colorDict = self.CreateColorDict()
		self.vertLst = gfx.vertex_list_indexed(4, [0, 1, 2, 0, 2, 3], 'v2i', 'c3B')
		self.changingColors = False

	def Place(self, dots):
		# Log("Placing a square on the window..", 3)
		for i in range(4):
			# Log("i = " + str(i), 4)
			# print(dots[i])
			# print(self.vertLst.vertices[i*2:(i*2+2)])
			self.vertLst.vertices[i*2:(i*2+2)] = dots[i]
			
	def PaintWhole(self, color):
		# Log("Painting the whole square..", 3)
		try:
			colVal = self.colorDict[color]
		except:
			print("NO SUCH COLOR!")
		for i in range(4):
			# Log("i = " + str(i), 4)
			self.vertLst.colors[i*3:(i*3+3)] = colVal
			
	def Draw(self):
		# Log("Drawing! ^_^", 3) #< bad idea to print to console anything at 60 FPS
		self.vertLst.draw(pyglet.gl.GL_TRIANGLES)
		
		if self.changingColors == True:
			self.colFlux.Change()
			colVal = self.colFlux.GetColors()
			for i in range(4):
				# Log("i = " + str(i), 4)
				# print("!!!!!!!")
				# print(colVal)
				# print(self.vertLst.colors[i*3:(i*3+3)])
				self.vertLst.colors[i*3:(i*3+3)] = colVal[i]
		else:
			Log("Static color", 2)
		
	def PaintFlux(self):
		# Log("Let the FUN begin!!", 3)
		self.changingColors = True
		self.colFlux = ChangingColors(4)
		colVal = self.colFlux.GetColors()
		for i in range(4):
			# Log("i = " + str(i), 4)
			# print("!!!!!!!")
			# print(colVal[i])
			# print(self.vertLst.colors[i*3:(i*3+3)])
			self.vertLst.colors[i*3:(i*3+3)] = colVal[i]

		
class ChangingColors(Color):
	def __init__(self, nodeNum):
		# Log("ChangingColors object is being created..", 2)
		minSpdChg = 1
		maxSpdChg = 7 - minSpdChg
		self.nodeNum = nodeNum
		self.nodeColors = self.RandomColor(nodeNum)
		# Log("Starting colors are: ", 3)
		Log(str(self.nodeColors), 3)
		self.nodColChgSpd = []
		for i in range(nodeNum):
			a = []
			for j in range(3):
				a += [int(rnd()*maxSpdChg+minSpdChg)]
			self.nodColChgSpd += [a]
		# Log("done!", 2)
	
	def GetColors(self):
		return self.nodeColors
	
	def Change(self):
		# change color for each node according to speed
		# Log("Changing colors...", 3)
		# Log("Old colors:", 4)
		Log(str(self.nodeColors),4)
		# Log("Change speeds:", 4)
		Log(str(self.nodColChgSpd),4)
		for i in range (self.nodeNum):
			for j in range(3):
				self.nodeColors[i][j] += self.nodColChgSpd[i][j]
				
				# if color limits are reached, invert speed
				if self.nodeColors[i][j] >= 255:
					self.nodeColors[i][j] = 255
					self.nodColChgSpd[i][j] = -self.nodColChgSpd[i][j]
				elif self.nodeColors[i][j] <= 0:
					self.nodeColors[i][j] = 0
					self.nodColChgSpd[i][j] = -self.nodColChgSpd[i][j]
	


# Graphics class for batched graphics
# class Graphics:
	# self.objects = []
	# self.objectCount = 0
	
	# def __init__(self):
		# self.batch = gfx.Batch()
	
	# def Draw():
		# self.batch.draw()
		
	# def AddColSquare():
		# self.objects += []
		
# RiseLogLevel(1)

window = pyglet.window.Window()
FPS = 60
figures = [False]

canvSizeX = 640
canvSizeY = 480

A = [0, 0]
B = [0, canvSizeY]
C = [canvSizeX, canvSizeY]
D = [canvSizeX, 0]

@window.event
def on_draw():
	if figures[0] == False:
		window.clear()
		sq = ColSquare()
		sq.Place( [A, B, C, D] )
		# sq.PaintWhole("white")
		sq.PaintFlux()
		figures[0] = sq
		sq.Draw()

def Frame(dt):
	# Log("\n\n\nNEW FRAME!!!\n\n\n")
	sq = figures[0]
	if sq.changingColors == True:
		window.clear()
		sq.Draw()
	
pyglet.clock.schedule_interval(Frame, 1/FPS)


pyglet.app.run()
