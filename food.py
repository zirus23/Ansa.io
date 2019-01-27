## Import Statements

import random
import pygame

## Food Class ##

class Food(object):
    gameDisplay = pygame.display.set_mode((1080, 720))

    def __init__(self, x, y, imageFood):
        self.width = 1080
        self.height = 720
        
        # Initialize a size between a min and max val
        # The size corresponds with the food mass
        minSize, maxSize = 10, 50
        self.size = random.randint(minSize, maxSize)

        self.img = imageFood 

        # self.x and self.y represent the (x,y) coordinates of the Food object
        self.x = x
        self.y = y
        
    def __repr__(self):
        return "mass = %d, x = %d, y = %d" % (self.size, self.x, self.y)
    
    def getSize(self):
        # Getter for the food's size
        return self.size
        
    def getPos(self):
        # Getter for the food's (x,y) location
        return (self.x, self.y)
    
    def collide(self):
        # Collision calls this function
        data.foodList.remove((self.size, self.x, self.y))

    def moveFood(self, dx, dy):
        # Scrolls the food by (dx,dy)
        self.x += dx
        self.y += dy
    
    def drawFood(self, screen):
        # Called from the canvas
        img = pygame.transform.scale(self.img, (self.size, self.size))
        Food.gameDisplay.blit(img, (self.x-self.size//2, self.y-self.size//2))