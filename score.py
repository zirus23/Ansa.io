#in init
#

######################score######################
self.score = 0

#VERIFY sizing
self.digitWidth = 10 
self.digitHeight = 20
self.scoreWidth = 100
self.scoreHeight = self.digitHeight
self.scoreX = 50
self.scoreY = 50
self.digitPadding = 5

#load images
self.scoreImg = pygame.image.load("images/score.png")
self.scoreImg = pygame.transform.scale(img, (self.scoreWidth, self.scoreHeight))

self.digitImages = []
for i in range(10): 
	img = pygame.image.load("images/digits/" + str(i) + ".png")
	img = pygame.transform.scale(img, (self.digitWidth, self.digitHeight))
	self.digitImages.append(pygame.image.load("images/digits/" + str(i) + ".png"))

####################################################################################################################################

##in main
def drawScore(self, screen):
	PygameGame.gameDisplay.blit(self.scoreImg, (self.scoreX, self.scoreY))
	numDigits = len(str(self.score))
	for i in range(numDigits):
		x = self.scoreX + self.scoreWidth + self.digitPadding + digitWidth*i
		PygameGame.gameDisplay.blit(self.digitImages[int(str(numDigits)[i])], (x, self.scoreY))