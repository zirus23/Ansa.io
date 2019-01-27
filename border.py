## Import Statements

import pygame
import globalData

## Border Class ##

class BorderGame(object):
	gameDisplay = pygame.display.set_mode((1080, 720))

	def __init__(self):
		self.width = 1080
		self.height = 720
		
		# (currX, currY) represents the top-left corner of the rectangular 
		# 	border
		self.currX = -self.width/2
		self.currY = -self.height/2

		# Initialize the right, left, bottom, and top border lines
		self.right = pygame.image.load("images/border/right.png")
		self.right = pygame.transform.scale(self.right, (40, self.height*2))
		self.left = pygame.image.load("images/border/left.png")
		self.left = pygame.transform.scale(self.left, (40, self.height*2))
		self.bottom = pygame.image.load("images/border/bottom.png")
		self.bottom = pygame.transform.scale(self.bottom, (self.width*2, 40))	
		self.top = pygame.image.load("images/border/top.png")
		self.top = pygame.transform.scale(self.top, (self.width*2, 40))	

		self.padding = 50 #CHANGE

	def getXY(self):
		# Getter for (currX,currY)
		return (self.currX, self.currY)
		
	def isLegal(self):
		
		# Checks if the current position of the border is legal
		# Padding is an estimate of the thickness of the border

		#20 accounts for border width
		#self.padding accounts for size of actual hero
		if (self.currX > self.width//2 - self.padding//2 - 20 or  #left hand boundary
			-self.currX > self.width*1.5 - self.padding//2 + 20): #right hand boundary
			return False
		if (self.currY > self.height//2 - self.padding//2 - 20 or #top boundary
			-self.currY > self.height*1.5 - self.padding//2 + 20): #bottom boundary
			return False
		return True
	
	def drawBorder(self, screen):
		# Draw the void
		gray = (171, 171, 171)
		pygame.draw.rect(screen, gray, 
						(self.currX - self.width/2, self.currY - self.height/2,
						self.width/2 + 30, self.height*3), 
						0)
		pygame.draw.rect(screen, gray, 
						(self.currX + self.width*2+20, self.currY - self.height/2,
						self.currX + self.width*2, self.height*3), 
						0)
		pygame.draw.rect(screen, gray, 
						(self.currX, self.currY - self.height/2, 
						self.currX + self.width*5, self.height/2 + 30), 
						0)
		pygame.draw.rect(screen, gray, 
						(self.currX, self.currY + self.height*2+20, 
						self.currX + self.width*5, self.currY + self.height*2), 
						0)

		# Draw the border
		BorderGame.gameDisplay.blit(self.right, (self.currX + self.width*2, self.currY))
		BorderGame.gameDisplay.blit(self.left, (self.currX,self.currY))
		BorderGame.gameDisplay.blit(self.bottom, (self.currX, self.currY + self.height*2))
		BorderGame.gameDisplay.blit(self.top, (self.currX, self.currY))
