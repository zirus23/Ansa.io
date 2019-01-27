## Import Statements

import pygame

import random, math, time

import numpy as np
import pandas as pd

from sklearn.cluster import KMeans

## AI Class ##

class AI(object):
	gameDisplay = pygame.display.set_mode((1080, 720))

	def __init__(self, color, x, y, startSize, currImage):
		self.color = color
		self.height = 720
		self.width = 1080
		self.size = startSize
		self.images = self.createImages()
		self.currImage = currImage
		self.pause = 0
		self.hitBox = 50

		self.x = x
		self.y = y
		
	def getHashables(self):
		return (self.color, self.x, self.y, self.size, self.currImage)
		
	def __hash__(self):
		return hash(self.getHashables())
		
	def __eq__(self, other):
		if isinstance(other, AI):
			if self.color == other.color and self.x == other.x and \
			self.y == other.y and self.size == other.size and self.currImage == other.currImage:
				return True
		return False

	def createImages(self):
		playerImages = []
		# Hero has 8 frames to cycle through
		for i in range(0,8):
			playerImages.append(pygame.image.load("images/" + self.color + "/" + str(i)+".png"))
		return playerImages

	def changeCurrImage(self):
		# Cycle to the next frame
		if self.currImage < 7 and self.pause == 4:
			self.currImage += 1
			self.pause = 0
		# Reset back to 0th frame when reached the last frame
		if self.currImage == 7: 
			self.currImage = 0
		self.pause += 1

	def moveAI(self, dx, dy):
		# Scrolls the food by (dx,dy)
		self.x += dx
		self.y += dy
		
	def getPos(self):
		# not used, use getInfo()
		return (self.x, self.y)
		
	def getInfo(self):
		return (self.x, self.y, self.size)

	def isLegal(self): 
		pass
		
	
	
	def findDestination(self, aiList, foodList, heroXYSize):
		# Returns the (x,y) destination for the AI as a tuple
		# Parameters:
		#   heroX and heroY represent the hero's current (x,y) location
		#   foodList is a list of tuples representing the food's (x,y) locations
		
		# Distance formula
		def distance(x1, y1, x2, y2):
			return math.sqrt((x1-x2)**2 + (y1-y2)**2)
			
		def findReflectedPoint(x1,y1,x2,y2):
			# Reflects (x1,y1) over (x2,y2)
			dx = x1 - x2
			dy = y1 - y2
			return (x1+2*dx, y1+2*dy)
			
		minDist = self.size*self.hitBox*3
		
		if distance(self.x, self.y, heroXYSize[0], heroXYSize[1]) < minDist*3:
			if self.size > heroXYSize[2]:
				return (heroXYSize[0], heroXYSize[1])
		
		ownInfo = (self.x, self.y, self.size)
		aiList.remove(ownInfo)
		for tup in aiList:
			if distance(self.x, self.y, tup[0], tup[1]) < minDist*3:
				# If you are bigger, chase
				if self.size > tup[2]:
					return tup
				# Else run away
				# else:
				# 	temp = findReflectedPoint(self.x, self.y, tup[0], tup[1])
				# 	if temp[0] > - self.width/2 and temp[0] < self.width/2 \
				# 	and temp[1] > -self.height/2 and temp[1] < self.height/2:
				# 		return temp
		
		# If any food is within minDist, move toward that food (no clustering)
		for tup in foodList:
			if distance(self.x, self.y, tup[0], tup[1]) < minDist:
				return tup
		
		if len(foodList) >= 4:
			# food_df is a pandas data frame with two cols (the x and y coordinates)
			food_df = pd.DataFrame()
			x, y = list(), list()
			for tup in foodList:
				x.append(tup[0])
				y.append(tup[1])
			food_df['x'] = x
			food_df['y'] = y
	
			# Run k-means clustering to cluster the food locations
			# 4 clusters was by personal choice
			kmeans = KMeans(n_clusters = 4, n_init = 4, max_iter = 1000)
			kmeans.fit(food_df)
			
			# Find the closest cluster
			leastDist, nearestCluster = math.inf, -1
			for clusterIndex in range(len(kmeans.cluster_centers_)):
				cluster = kmeans.cluster_centers_[clusterIndex]
				if distance(self.x, self.y, cluster[0], cluster[1]) < leastDist:
					leastDist = distance(self.x, self.y, cluster[0], cluster[1])
					nearestCluster = clusterIndex
			return tuple(kmeans.cluster_centers_[nearestCluster])
		elif len(foodList) > 0:
			leastDist, nearestIndex = math.inf, -1
			for i in range(len(foodList)):
				tup = foodList[i]
				if distance(self.x, self.y, tup[0], tup[1]) < leastDist:
					leastDist = distance(self.x, self.y, tup[0], tup[1])
					nearestIndex = i
			return foodList[nearestIndex]
		else:
			# No food, stay put
			return (self.x, self.y)
		
	def findDxDy(self, aiList, foodList, heroXYSize):
		loc = self.findDestination(aiList, foodList, heroXYSize)
		distanceVec = (loc[0] - self.x, loc[1] - self.y)
		distanceVecNorm = (distanceVec[0]**2 + distanceVec[1]**2)**0.5
		try:
			unitDistanceVec = (distanceVec[0] / distanceVecNorm, distanceVec[1] / distanceVecNorm)
		except:
			unitDistanceVec = (0,0)
		# Moves 10 units (supposed to be equal to self.move from pyMain)
		try:
			return (int(unitDistanceVec[0] * 10), int(unitDistanceVec[1] * 10))
		except:
			return (0,0)
		
	def getSize(self):
		return int(self.size * self.hitBox)

	def drawAI(self, screen):
		currSize = self.getSize()
		img = pygame.transform.scale(self.images[self.currImage], (currSize, currSize))
		AI.gameDisplay.blit(img, (self.x - currSize//2, self.y - currSize//2))

