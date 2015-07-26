import tkinter as tk # GUI
from math import sqrt
from random import Random
randGen = Random() # Random number generator

if __name__ == '__main__' : # A user is attempting to run this file directly...
	raise SystemExit("This isn't the entry point - please run main.py instead!")

"""Create an independent copy of the given table (dictionary)."""
def copyTable(t) :
	r = {}
	for i in range(0,len(t)) :
		r[i] = t[i]
	return r

	
"""The field of nodes (cities). This is implemented as a drawing canvas for simplicity."""
class Field(tk.Canvas) :
	def __init__(self, w=640, h=480, padRatio=0.05, mstr=None) :
		tk.Canvas.__init__(self, width=w, height=h, master=mstr, background='#ffc')
		self.width = w
		self.height = h
		self.nodeMap = None # This will hold the X and Y co-ordinates of all the nodes in the field.
		self.grid(padx=w*padRatio, pady=h*padRatio)
		
	"""Generates a given number of nodes, distributes them randomly on the field
	and stores them in self.nodeMap in the order they were created. The total travel
	distance is calculated and stored in self.curMinDist."""
	def generateNodes(self, count=20) :
		# Delete any existing nodes.
		self.delete('node')
		self.nodeMap = {}
		
		self.createNode(8, '#f00') # The first node to be created is emphasised, for some reason.
		for i in range(0, count-1) :
			self.createNode(4, '#000')
			
		self.linkNodes()
		self.curMinDist = self.getTotalDistance(self.nodeMap)
	
	"""Tries to decrease the total travel distance between all of the nodes by swapping the order in
	which two of them are visited. Returns true if a shorter arrangement of nodes was found, or false if
	no shorter arrangemnt could be found after a certain number of attempts."""
	def randomSwap(self) :
		if (self.nodeMap==None) : return # No nodes exist yet.
		
		candDist = None # The total travel distance for the candidate map, with two randomly swapped nodes.
		attempts = 0 # The number of times we've tried to find a lower travel distance. If this passes a threshold, we give up and return false.
		
		# Keep swapping random pairs of nodes until we find an arrangement that shortens the travel distance or until we reach the attempts threshold.
		while (candDist == None or candDist >= self.curMinDist) :
			attempts += 1
			if (attempts == len(self.nodeMap)*100) : # We make up to 100 attempts for every node in the field.
				# Give up on finding a shorter path and return false.
				return False
			else :
				# Choose two different nodes at random.
				nA = None
				nB = None
				while nA == nB :
					nA = randGen.randint(0, len(self.nodeMap)-1)
					nB = randGen.randint(0, len(self.nodeMap)-1)
				
				# Create a local copy of the node map.
				candMap = copyTable(self.nodeMap)
					
				# Swap the positions of the two selected nodes.
				tA = self.nodeMap[nB]
				candMap[nA] = tA
				tB = self.nodeMap[nA]
				candMap[nB] = tB
						
				candDist = self.getTotalDistance(candMap)

		# If we reach this point, we have found a better solution, so...
		self.nodeMap = copyTable(candMap) # ...record the candidate map as the new best map...
		self.curMinDist = candDist # ...record the new (lower) total travel distance...
		self.linkNodes() # ...repaint the links between the nodes...
		return True # ...and return true to indicate our success.
	
	def createNode(self, size, colour) :
		radius = size / 2
		
		# Choose a random location in the field to create the node at.
		x = randGen.randint(0, self.width)
		y = randGen.randint(0, self.height)
		
		self.create_rectangle(x - radius, y - radius, x + radius, y + radius, fill=colour, tag='node')
		
		self.nodeMap[len(self.nodeMap)] = {"x": x, "y": y} # Append these co-ordinates onto the end of the list.
		
	def getTotalDistance(self, m) :
		totalDistance = 0
		
		for nId in range(0, len(m)) :
			nCur = m[nId]
			nNext = m[(nId+1) % len(m)] # At the very last node, this will wrap round back to the starting node (index 0).
			
			# Using Pythagoras' theorem to determine the distance between this node and the next.
			totalDistance += sqrt( (nCur["x"] - nNext["x"])**2 + (nCur["y"] - nNext["y"])**2 )
			
		return totalDistance
		
	"""Visually links the nodes together in the order they are listed in self.nodeMap"""
	def linkNodes(self) :
		self.delete('link') # Delete all existing links, if any.
		
		for nId in range(0, len(self.nodeMap)) :
			nCur = self.nodeMap[nId]
			nNext = self.nodeMap[(nId+1) % len(self.nodeMap)]
			
			self.create_line(nCur["x"], nCur["y"], nNext["x"], nNext["y"], fill='#030', tag='link', arrow=tk.FIRST)