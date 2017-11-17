import pyglet
from pyglet import graphics as gfx

from numpy.random import random as rnd

# from other.log import RiseLogLevel, LogIt as Log


# HowTo:
# 1. Create
# 2. Place
# 3. Draw

# Created mainly coz I'm lazy. Can be used to generate random int color values (0 .. 255).
class Color:
	# returns a variable that has "all colors you may need". That or just white. Again, coz I'm lazy.
	def CreateColorDict(self):
		colorDict = {
			"white" : [255, 255, 255]
			}
		return colorDict
		
	# returns a random integer value (0 .. 255)
	def RndColVal(self):
		return int(rnd()*256)
		
	# returns a list of random color values.
	# Actually, a list of lists.
	# Takes number of [RGB] lists to return as nodeNum parameter
	def RandomColor(self, nodeNum = 1):
			# Log("Generating random node colors...", 3)
			ret = []
			for i in range(nodeNum):
				ret += [[self.RndColVal(), self.RndColVal(), self.RndColVal()]]
			return ret
		
		
# Creates a colored square (or a rect. does not care as long as you put in 4 dots) (what a surprise!)
class ColSquare(Color):
	def __init__(self):
		# Log("A square has been created!", 2)
		self.colorDict = self.CreateColorDict()
		self.vertLst = gfx.vertex_list_indexed(4, [0, 1, 2, 0, 2, 3], 'v2i', 'c3B')
		self.changingColors = False

	# adds vertices to a vertices list. Sort of tells what place to take.
	# Takes a list of [X, Y] lists. (each 4 dots of a rectangle have to be listed)
	def Place(self, dots):
		# Log("Placing a square on the window..", 3)
		for i in range(4):
			self.vertLst.vertices[i*2:(i*2+2)] = dots[i]
			
	# Can paint the whole rectangle in %color%
	# color is a string name from colotDict dictionary
	def PaintWhole(self, color):
		# Log("Painting the whole square..", 3)
		try:
			colVal = self.colorDict[color]
		except:
			print("NO SUCH COLOR!")
		for i in range(4):
			# Log("i = " + str(i), 4)
			self.vertLst.colors[i*3:(i*3+3)] = colVal
			
	# Draws rectangle and refreshes it's colors if they have to be refreshed.
	def Draw(self):
		# Log("Drawing! ^_^", 3) #< bad idea to print to console anything at 60 FPS
		self.vertLst.draw(pyglet.gl.GL_TRIANGLES)
		
		if self.changingColors == True:
			self.colFlux.Change()
			colVal = self.colFlux.GetColors()
			for i in range(4):
				self.vertLst.colors[i*3:(i*3+3)] = colVal[i]
		else:
			# Log("Static color", 2)
			pass
	# The same as PaintWhole just so much more fun.
	def PaintFlux(self):
		# Log("Let the FUN begin!!", 3)
		self.changingColors = True
		self.colFlux = ChangingColors(4)
		colVal = self.colFlux.GetColors()
		for i in range(4):
			self.vertLst.colors[i*3:(i*3+3)] = colVal[i]

# I should someday remake it to become a parent class. Really.
# Creates an object that can manipulate colors and stores color values. Handy!
class ChangingColors(Color):
	def __init__(self, nodeNum):
		# Log("ChangingColors object is being created..", 2)
		minSpdChg = 1
		maxSpdChg = 7 - minSpdChg
		self.nodeNum = nodeNum
		self.nodeColors = self.RandomColor(nodeNum)
		# Log("Starting colors are: ", 3)
		# Log(str(self.nodeColors), 3)
		self.nodColChgSpd = []
		for i in range(nodeNum):
			a = []
			for j in range(3):
				a += [int(rnd()*maxSpdChg+minSpdChg)]
			self.nodColChgSpd += [a]
		# Log("done!", 2)
		
	# Gives colors!
	def GetColors(self):
		return self.nodeColors
	
	# Fluidly changes colors
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
	



		
# RiseLogLevel(1)

# Creates the window
window = pyglet.window.Window()
FPS = 60
figures = [False]

# Ugh.. almost unused
canvSizeX = 640
canvSizeY = 480

# Just to make it easier to reshape a rectangle
A = [0, 0]
B = [0, canvSizeY]
C = [canvSizeX, canvSizeY]
D = [canvSizeX, 0]

# called each time smth is drawn. Should use something else here, possibly...
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

# Used to change frames.
def Frame(dt):
	# Log("\n\n\nNEW FRAME!!!\n\n\n")
	sq = figures[0]
	if sq.changingColors == True:
		window.clear()
		sq.Draw()
	
# calls Frame each 1/FPS seconds
pyglet.clock.schedule_interval(Frame, 1/FPS)

# where would we be without this one?
pyglet.app.run()
