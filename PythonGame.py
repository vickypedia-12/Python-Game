import pygame 
import sys
import os
import random
import math

pygame.init()
pygame.display.set_caption("Snake Game")
pygame.font.init()
random.seed()


SPEED = 0.36
SNAKE_SIZE = 9
APPLE_SIZE = SNAKE_SIZE
SEPARATION = 10
SCREEN_HEIGHT = 600
SCREEN_WIDTH = 800
FPS = 25
KEY = {"UP" : 1, "DOWN" : 2, "LEFT" : 3,"RIGHT" : 4}

screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT),pygame.HWSURFACE)

scoreFont = pygame.font.Font(None,38)
scoreNumbFont = pygame.font.Font(None,28)
gameOverFont = pygame.font.Font(None,46)
playAgainFont = scoreNumbFont
scoreMsg = scoreFont.render("Score : ",1,pygame.Color("green"))
scoreMsgSize = scoreFont.size("Score")
backgroundColor = pygame.Color(0,0,0)
black = pygame.Color(0,0,0)

gameClock = pygame.time.Clock()

def checkCollision(posA,As , posB,Bs):
    if(posA.x < posB.x+Bs and posA.x+As > posB.x and posA.y < posB.y+Bs and posA.y+As > posB.y):
        return True
    return False

def checkLimits(snake):
    if(snake.x > SCREEN_WIDTH):
        snake.x = SNAKE_SIZE
    if(snake.x < 0):
        snake.x = SCREEN_WIDTH - SNAKE_SIZE
    if(snake.y > SCREEN_HEIGHT):
        snake.y = SNAKE_SIZE
    if(snake.y<0):
        snake.y = SCREEN_HEIGHT - SNAKE_SIZE

class Apple:
    def __init__(self,x,y,state):
        self.x = x
        self.y = y
        self.state = state
        self.color = pygame.color.Color("orange")
        
    def draw(self,screen):
        pygame.draw.rect(screen,self.color,(self.x,self.y,APPLE_SIZE,APPLE_SIZE),0)

class segment:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.direction = KEY["UP"]
        self.color = "white"

class snake:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.direction = KEY["UP"]
        self.stack = []
        self.stack.append(self)
        blackBox = segment(self.x , self.y + SEPARATION)
        blackBox.direction = KEY["UP"]
        blackBox.color = "NULL"
        self.stack.append(blackBox)
        
#moves definiton
        
    def move(self):
        last_element = len(self.stack) - 1
        while(last_element != 0):
            self.stack[last_element].direction = self.stack[last_element-1].direction
            self.stack[last_element].x = self.stack[last_element-1].x
            self.stack[last_element].y = self.stack[last_element-1].y
            last_element-=1
        if(len(self.stack)<2):
            lastSegment = self
        else:
            lastSegment = self.stack.pop(last_element)
            lastSegment.direction = self.stack[0].direction
        if(self.stack[0].direction == KEY["UP"]):
            lastSegment.y = self.stack[0].y - (SPEED * FPS)
        elif(self.stack[0].direction == KEY["DOWN"]):
            lastSegment.y = self.stack[0].y + (SPEED * FPS)
        elif(self.stack[0].direction == KEY["LEFT"]):
            lastSegment.x = self.stack[0].x - (SPEED * FPS) 
        elif(self.stack[0].direction == KEY["RIGHT"]):
            lastSegment.x = self.stack[0].x + (SPEED * FPS)
        self.stack.insert(0,lastSegment)
            
    def gethead(self):
        return(self.stack[0])
    
    def grow(self):
        last_element = len(self.stack) - 1
        self.stack[last_element].direction = self.stack[last_element].direction
        if(self.stack[last_element].direction == KEY["UP"]):
            newSegment = segment(self.stack[last_element].x, self.stack[last_element].y - SNAKE_SIZE)
            blackBox = segment(newSegment.x, newSegment.y - SEPARATION)
            
        elif(self.stack[last_element].direction == KEY["DOWN"]):
            newSegment = segment(self.stack[last_element].x, self.stack[last_element].y + SNAKE_SIZE)
            blackBox = segment(newSegment.x, newSegment.y + SEPARATION)
           
        elif(self.stack[last_element].direction == KEY["LEFT"]):
            newSegment = segment(self.stack[last_element].x - SNAKE_SIZE, self.stack[last_element].y)
            blackBox = segment(newSegment.x - SEPARATION, newSegment.y)
        
        elif(self.stack[last_element].direction == KEY["RIGHT"]):
            newSegment = segment(self.stack[last_element].x + SNAKE_SIZE, self.stack[last_element].y)
            blackBox = segment(newSegment.x + SEPARATION, newSegment.y)             
        
        blackBox.color = "NULL"
        self.stack.append(newSegment)
        self.stack.append(blackBox)
        
    def iterateSegments(self,delta):
        pass
        
    def setDirection(self,direction):
        if(self.direction == KEY["RIGHT"] and direction == KEY["LEFT"] or self.direction == KEY["LEFT"] and direction == KEY["RIGHT"]):
            pass
        elif(self.direction == KEY["UP"] and direction == KEY["DOWN"] or self.direction == KEY["UP"] and direction == KEY["DOWN"]):
            pass
        else:
            self.direction = direction
    
    def getRect(self):
        rect = (self.x , self.y)
        return rect
    
    def getX(self):
        return self.x
    
    def getY(self):
        return self.y
    
    def setX(self,x):
        self.x = x
        
    def setY(self,y):
        self.y = y
    
    def checkCrashing(self):
        counter = 1
        while(counter < len(self.stack)-1):
            if(checkCollision(self.stack[0],SNAKE_SIZE,self.stack[counter],SNAKE_SIZE) and self.stack[counter].color != "NULL"):
                return True
            counter +=1
        return False
    
    
    def draw(self,screen):
        pygame.draw.rect(screen,pygame.color.Color("green"),(self.stack[0].x, self.stack[0].y,SNAKE_SIZE,SNAKE_SIZE),0)
        counter = 1
        while(counter < len(self.stack)):
            if(self.stack[counter].color == "NULL"):
                counter +=1
                continue
            pygame.draw.rect(screen , pygame.color.Color("yellow"), (self.stack[counter].x,self.stack[counter].y,SNAKE_SIZE,SNAKE_SIZE),0)
            counter+=1

def getKey():
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                return KEY["UP"]
            elif event.key == pygame.K_DOWN:
                return KEY["DOWN"]
            elif event.key == pygame.K_LEFT:
                return KEY["LEFT"]
            elif event.key == pygame.K_RIGHT:
                return KEY["RIGHT"]
            
            elif event.key == pygame.K_ESCAPE:
                return "exit"
            
            elif event.key == pygame.K_y:
                return "yes"
            
            elif event.key == pygame.K_n:
                return "no"   
        if event.type == pygame.QUIT:
            sys.exit(0)
            
            
def endGame():
    message = gameOverFont.render("Game Over",1,pygame.Color("white"))
    messagePlayAgain = playAgainFont.render("Play Again?(Y/N)", 1, pygame.Color("green"))
    screen.blit(message,(320,240))
    screen.blit(messagePlayAgain,(320+12,240+40))
    
    pygame.display.flip()
    pygame.display.update()
    
    mKey = getKey()
    while(mKey != "exit"):
        if(mKey == "yes"):
            main()
        elif(mKey == "no"):
            break
        mKey = getKey()
        gameClock.tick(FPS)
    sys.exit(0)
    
def drawScore(score):
    scoreNumb = scoreNumbFont.render(str(score),1,pygame.Color("red"))
    screen.blit(scoreMsg, (SCREEN_WIDTH - scoreMsgSize[0]-60,10))
    screen.blit(scoreNumb,(SCREEN_WIDTH-45,14))
    
def drawGameTime(gameTime):
    gameTimeText = scoreFont.render("Time:", 1,pygame.Color("white"))
    gameTimeNumb = scoreNumbFont.render(str(gameTime // 1000),1,pygame.Color("white"))
    screen.blit(gameTimeText,(30,10))
    screen.blit(gameTimeNumb,(105,14))
    
def exitScreen():
    pass
    
def respawnApple(apples , index , sx, sy):
    radius = math.sqrt((SCREEN_WIDTH/2*SCREEN_WIDTH/2 + SCREEN_HEIGHT/2*SCREEN_HEIGHT/2))/2 
    angle = 999
    while(angle > radius):
        angle = random.uniform(0,800)*math.pi*2
        x = SCREEN_WIDTH/2 + radius * math.cos(angle)
        y = SCREEN_HEIGHT/2 + radius * math.sin(angle)
        if(x == sx and y == sy):
            continue
    newApple = Apple(x ,y, 1)
    apples[index] = newApple
    
def respawnApples(apples , quantity , sx, sy):
    counter = 0
    del apples[:]
    radius = math.sqrt((SCREEN_WIDTH/2*SCREEN_WIDTH/2 + SCREEN_HEIGHT/2*SCREEN_HEIGHT/2))/2 
    angle = 999
    while(counter < quantity):
        while(angle > radius):
            angle = random.uniform(0,800)*math.pi*2
            x = SCREEN_WIDTH/2 + radius * math.cos(angle)
            y = SCREEN_HEIGHT/2 + radius * math.sin(angle)
            if((x-APPLE_SIZE == sx or x+APPLE_SIZE ==sx) and (y-APPLE_SIZE == sy or y + APPLE_SIZE == sy) or radius - angle <=10):
                continue
        apples.append(Apple(x,y,1))
        angle = 999
        counter+=1        
    
def main():
    score = 0
    
    mySnake = snake(SCREEN_WIDTH/2,SCREEN_HEIGHT/2)
    mySnake.setDirection(KEY["UP"])
    mySnake.move()
    startSegments = 3
    while(startSegments > 0):
        mySnake.grow()
        mySnake.move()
        startSegments -=1
        
    maxApples = 1
    eatenApple = False
    apples = [Apple(random.randint(60,SCREEN_WIDTH),random.randint(60,SCREEN_HEIGHT),1)]
    respawnApples(apples,maxApples, mySnake.x, mySnake.y)
    
    startTime = pygame.time.get_ticks()
    endgame = 0
    
    while(endgame != 1):
        gameClock.tick(FPS)
        
        keyPress = getKey()
        if keyPress == "exit":
            endgame = 1
            
        checkLimits(mySnake)
        if(mySnake.checkCrashing() == True):
            endGame()
            
        for myApple in apples:
            if(myApple.state == 1):
                if(checkCollision(mySnake.gethead(), SNAKE_SIZE,myApple, APPLE_SIZE) == True):
                    mySnake.grow()
                    myApple.state = 0
                    score += 10
                    eatenApple = True
                    
        if(keyPress):
            mySnake.setDirection(keyPress)
        mySnake.move()
        
        if(eatenApple == True):
            eatenApple = False
            respawnApple(apples, 0, mySnake.gethead().x, mySnake.gethead().y)
            
            
        screen.fill(backgroundColor)
        for myApple in apples:
            if(myApple.state == 1):
                myApple.draw(screen)
                
        mySnake.draw(screen)
        drawScore(score)
        gameTime = pygame.time.get_ticks() - startTime
        drawGameTime(gameTime)
        
        pygame.display.flip()
        pygame.display.update()
            
main()