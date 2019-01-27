## Import Files

# Modules
import pygame
import random
import copy
# import pyaudio

# Other project files
import globalData
import hero
import border
import aiPlayer
from food import Food

## Game Class ##

class PygameGame(object):
    gameDisplay = pygame.display.set_mode((1080, 720))

    def init(self):
        self.width = 1080
        self.height = 720
        self.player = hero.HeroPlayer("b", 1, 0)
        self.border = border.BorderGame()
        
        self.startX = 466
        self.startY = 550
        self.startRadius = 55
        self.state = "Start"
        
        self.heroX = self.width // 2
        self.heroY = self.height // 2

        self.left = False
        self.right = False
        self.up = False
        self.down = False
        
        self.startFrame = 0
        self.startTimer = 0

        self.move = 10 ###CHANGE

        self.pause = 0

        self.foodImages = []
        for i in range(15):
            self.foodImages.append(pygame.image.load("images/food/f" + str(i)+".png"))

        self.foodList = []
        while (len(self.foodList) <= 50):
            self.genFood()

        self.aiPlayers = []
        
        pygame.init()

    def mousePressed(self, x, y):
        self.startGame(x, y)

    def mouseReleased(self, x, y):
        pass

    def mouseMotion(self, x, y):
        pass

    def mouseDrag(self, x, y):
        pass

    def keyPressed(self, keyCode, modifier):
        if keyCode == pygame.K_LEFT: 
            self.left = True
            self.heroX -= self.move
        if keyCode == pygame.K_RIGHT: 
            self.right = True
            self.heroX += self.move
        if keyCode == pygame.K_UP: 
            self.up = True
            self.heroY -= self.move
        if keyCode == pygame.K_DOWN: 
            self.down = True
            self.heroY += self.move
        if keyCode == pygame.K_SPACE and self.state == 'End': 
            self.init()

    def keyReleased(self, keyCode, modifier):
        if keyCode == pygame.K_LEFT: self.left = False
        if keyCode == pygame.K_RIGHT: self.right = False
        if keyCode == pygame.K_UP: self.up = False
        if keyCode == pygame.K_DOWN: self.down = False

    def startGame(self, userX, userY):
        #distance between center of start button and user click
        distance = ((userX - self.startX)**2 + (userY - self.startY)**2)**(1/2)
        #click was within border of target
        if distance <= self.startRadius:
            self.state = "Play"
            return True
        else: return False
    
    def changeStartImage(self):
        if self.startFrame == 0:
            self.startFrame = 1
        else:
            self.startFrame = 0
    
    def getHeroXYSize(self):
        return (self.heroX, self.heroY, self.player.size)
    
    def timerFired(self, dt):
        if self.state == 'Play':
            self.player.changeCurrImage()
            for ai in self.aiPlayers:
                ai.changeCurrImage()
            if self.right: 
                self.border.currX -= self.move
                if not self.border.isLegal():
                    self.border.currX += self.move
                else:
                    for food in self.foodList:
                        food.moveFood(-self.move, 0)
                    for player in self.aiPlayers:
                        player.moveAI(-self.move,0)

                    
            if self.left: 
                self.border.currX += self.move
                if not self.border.isLegal():
                    self.border.currX -= self.move
                else:
                    for food in self.foodList:
                        food.moveFood(self.move, 0)
                    for player in self.aiPlayers:
                        player.moveAI(self.move,0)
             
    
            if self.down: 
                self.border.currY -= self.move
                if not self.border.isLegal():
                    self.border.currY += self.move
                else:
                    for food in self.foodList:
                        food.moveFood(0, -self.move)
                    for player in self.aiPlayers:
                        player.moveAI(0, -self.move)
                
    
            if self.up: 
                self.border.currY += self.move
                if not self.border.isLegal():
                    self.border.currY -= self.move
                else:
                    for food in self.foodList:
                        food.moveFood(0, self.move)
                    for player in self.aiPlayers:
                        player.moveAI(0, self.move)
                
            
            # Hero colliding with food
            isCollidingWithFood = False
            # currFood is a list of food currently in contact
            self.currFood = []
            for food in self.foodList:
                size, x, y = food.size, food.x, food.y
                if x > self.width/2 - (self.player.size * self.player.hitBox)/2 and x < self.width/2 + (self.player.size * self.player.hitBox)/2:
                    if y > self.height/2 - (self.player.size * self.player.hitBox)/2 and y < self.height/2 + (self.player.size * self.player.hitBox)/2:
                        isCollidingWithFood = True
                        self.currFood.append(food)
            if isCollidingWithFood == True:
                for food in self.currFood:
                    # Remove the food being collided with from foodList
                    self.foodList.remove(food)
                    # Update hero size
                    if self.player.size <= 6: 
                        self.player.size += 0.01*(food.size)**0.5        
            
            # AI colliding with food
            self.currFood = []
            for player in self.aiPlayers:
                isCollidingWithFood = False
                for food in self.foodList:
                    size, x, y = food.size, food.x, food.y
                    if x > player.x - (player.size*player.hitBox)/2 and x < player.x + (player.size*player.hitBox)/2:
                        if y > player.y - (player.size*player.hitBox)/2 and y < player.y + (player.size*player.hitBox)/2:
                            isCollidingWithFood = True
                            self.currFood.append(food)
                if isCollidingWithFood == True:
                    for food in self.currFood:
                        if food in self.foodList:
                            self.foodList.remove(food)
                            if player.size <= 6: 
                                player.size += 0.01*(food.size)**0.5
                
    
            # Hero colliding with AI
            isCollidingWithPlayer = False
            # currPlayer is a list of players currently in contact
            self.currPlayer = []
            for player in self.aiPlayers:
                size, x, y = player.size, player.x, player.y
                if x > self.width/2 - (self.player.size * self.player.hitBox)/2 and x < self.width/2 + (self.player.size * self.player.hitBox)/2:
                    if y > self.height/2 - (self.player.size * self.player.hitBox)/2 and y < self.height/2 + (self.player.size * self.player.hitBox)/2:
                        isCollidingWithPlayer = True
                        self.currPlayer.append(player)
            if isCollidingWithPlayer == True:
                # Remove the AI players
                for player in self.currPlayer:
                    if self.player.size > player.size:
                        self.aiPlayers.remove(player)
                        if self.player.size <= 6: 
                            self.player.size += 0.01*(player.size)**0.5
                    else:
                        # GAME OVER CONDITIONS
                        self.state = 'End'
                            
            # AI colliding with AI
            for player1 in self.aiPlayers:
                isCollidingWithAI = False
                self.currPlayer = []
                for player2 in self.aiPlayers:
                    size1, x1, y1 = player1.size, player1.x, player1.y
                    size2, x2, y2, hitBox2 = player2.size, player2.x, player2.y, player2.hitBox
                    if x1 > x2 - (size2*hitBox2)/2 and x1 < x2 + (size2*hitBox2)/2:
                        if y1 > y2 - (size2*hitBox2)/2 and y1 < y2 + (size2*hitBox2)/2:
                            if player1 != player2:
                                isCollidingWithAI = True
                                if size1 > size2:
                                    self.currPlayer.append(player2)
                                    if player1.size <= 6: 
                                        player1.size += 0.01*(food.size)**0.5
                                else:
                                    self.currPlayer.append(player1)
                                    if player2.size <= 6:
                                        player2.size += 0.01*(food.size)**0.5
                self.currPlayer = list(set(self.currPlayer))
                if isCollidingWithAI == True:
                    for player in self.currPlayer:
                        self.aiPlayers.remove(player)
            
            # Update border padding
            maxSize = 0
            maxHitBox = 0
            for player in self.aiPlayers:
                if player.size*player.hitBox > maxSize*maxHitBox:
                    maxSize = player.size
                    maxHitBox = player.hitBox
            # Take the biggest out of all AIs and compare to hero as well
            newBorderPadding = max(maxSize*maxHitBox, self.player.size*self.player.hitBox)
            self.border.padding = newBorderPadding
            
            # Move AIs
            # Make a list of tuples of food (x,y) locs
            foodXY = list()
            for food in self.foodList:
                foodXY.append(food.getPos())
            
            # Make a list of tuples of AI (x,y,size)
            aiXYSize = list()
            for player in self.aiPlayers:
                aiXYSize.append(player.getInfo())
            aiXYSize.append((self.width/2, self.height/2, self.player.size))
            
            heroXYSize = self.getHeroXYSize()
            
            for player in self.aiPlayers:
                (dx, dy) = player.findDxDy(aiXYSize, foodXY, heroXYSize)
                player.moveAI(dx,dy)
            
            if self.pause == 10: 
                self.genFood()
                self.genAI()
                self.pause = 0
            else: self.pause += 1
        elif self.state == 'Start':
            self.startTimer += 1
            if self.startTimer % 4 == 0:
                self.changeStartImage()
            

    def genAI(self):
        (borderX, borderY) = self.border.getXY()
        padding = 29
        def isLegal(x,y):
            return x > borderX + padding and x < borderX + 2*self.width - padding \
            and y > borderY + padding and y < borderY + 2*self.height - padding
        screenLeft = -self.width/2
        screenRight = self.width*1.5
        screenTop = -self.height/2
        screenBottom = self.height*1.5
        x = random.randint(screenLeft, screenRight)
        y = random.randint(screenTop, screenBottom)
        while not isLegal(x,y):
            x = random.randint(screenLeft, screenRight)
            y = random.randint(screenTop, screenBottom)
        
        newAI = aiPlayer.AI("r", x, y, 1, 0) #color, x y coords, start size, start index of image
        if len(self.aiPlayers) < 10:
            self.aiPlayers.append(newAI)
        

    def genFood(self):
        randIndex = random.randint(0, 14)
        (borderX, borderY) = self.border.getXY()
        padding = 29
        def isLegal(x,y):
            return x > borderX + padding and x < borderX + 2*self.width - padding \
            and y > borderY + padding and y < borderY + 2*self.height - padding
        screenLeft = -self.width/2
        screenRight = self.width*1.5
        screenTop = -self.height/2
        screenBottom = self.height*1.5
        x = random.randint(screenLeft, screenRight)
        y = random.randint(screenTop, screenBottom)
        while not isLegal(x,y):
            x = random.randint(screenLeft, screenRight)
            y = random.randint(screenTop, screenBottom)
        
        curr = Food(x, y, self.foodImages[randIndex])
        if len(self.foodList) < 100:
            self.foodList.append(curr)  

    def redrawAll(self, screen):
        if self.state == "Start":
            img = pygame.image.load("images/start" + str(self.startFrame) + ".png")
            img = pygame.transform.scale(img, (self.width, self.height))
            PygameGame.gameDisplay.blit(img, (0,0))
        elif self.state == 'Play':
            self.border.drawBorder(screen)
            self.drawFoodPieces(screen)
            self.player.drawHero(screen)
            self.drawAIPlayers(screen)
        elif self.state == 'End':
            self.border.drawBorder(screen)
            img = pygame.image.load("images/gameover.png")
            img = pygame.transform.scale(img, (self.width, self.height))
            PygameGame.gameDisplay.blit(img, (0,0))
            self.drawFoodPieces(screen)
            self.player.drawHero(screen)
            self.drawAIPlayers(screen)
            
    def drawAIPlayers(self, screen):
        for player in self.aiPlayers:
            player.drawAI(screen)

    def drawFoodPieces(self, screen):
        for item in self.foodList:
            #Calling the def in the class
            item.drawFood(screen)

    def isKeyPressed(self, key):
        ''' return whether a specific key is being held '''
        return self._keys.get(key, False)

    
    def __init__(self, width=1080, height=720, fps=50, title="112 Pygame Game"):
        self.width = width
        self.height = height
        self.fps = fps
        self.title = title
        self.bgColor = (255, 255, 255)
        #background music
        pygame.init()
    

    def run(self):

        clock = pygame.time.Clock()
        screen = pygame.display.set_mode((self.width, self.height))
        # set the title of the window
        pygame.display.set_caption(self.title)

        # stores all the keys currently being held down
        self._keys = dict()
    
        # pygame.mixer.pre_init(44100,16,2,4096)
        # pygame.mixer.music.load("ansa.wav")
        # pygame.mixer.music.set_volume(0.5)
        # pygame.mixer.music.play(-1)

        # call game-specific initialization
        self.init()
        playing = True
        while playing:
            time = clock.tick(self.fps)
            self.timerFired(time)
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.mousePressed(*(event.pos))
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    self.mouseReleased(*(event.pos))
                elif (event.type == pygame.MOUSEMOTION and
                      event.buttons == (0, 0, 0)):
                    self.mouseMotion(*(event.pos))
                elif (event.type == pygame.MOUSEMOTION and
                      event.buttons[0] == 1):
                    self.mouseDrag(*(event.pos))
                elif event.type == pygame.KEYDOWN:
                    self._keys[event.key] = True
                    self.keyPressed(event.key, event.mod)
                    
                elif event.type == pygame.KEYUP:
                    self._keys[event.key] = False
                    self.keyReleased(event.key, event.mod)
                elif event.type == pygame.QUIT:
                    playing = False

                    
            screen.fill(self.bgColor)
            self.redrawAll(screen)
            pygame.display.flip()

        pygame.quit()


def main():
    class Struct(): pass
    data = Struct()
    data.height = 720
    data.width = 1080
    game = PygameGame()
    game.run()

if __name__ == '__main__':
    main()

