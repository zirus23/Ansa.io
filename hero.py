## Import Statements

import pygame

## Hero Class ##

class HeroPlayer(object):
	gameDisplay = pygame.display.set_mode((1080, 720))

	def __init__(self, color, startSize, currImage):
		self.color = color
		self.height = 720
		self.width = 1080
		self.size = startSize
		self.images = self.createImages()
		self.currImage = currImage
		self.pause = 0
		self.hitBox = 50 ##CHANGE #pixel size of drawing

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

	def getSize(self):
		return int(self.size * self.hitBox)

	def drawHero(self, screen):
		currSize = self.getSize()
		img = pygame.transform.scale(self.images[self.currImage], (currSize, currSize))
		HeroPlayer.gameDisplay.blit(img, (self.width//2 - currSize//2, self.height//2 - currSize//2))

