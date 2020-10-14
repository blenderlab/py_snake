'''
SNAKE GAME
Author : Thomas HOCEDEZ
 
 Requirements : 
    Python 3.8 
    Pygame
'''

import pygame
import sys
import time
import random

#directions
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4


# Colors
red = pygame.Color(255, 20, 20)
green = pygame.Color(20, 255,20)
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
brown = pygame.Color(20, 22, 22)

# Pygame Init
init_status = pygame.init()

if init_status[1] > 0:
    print("(!) Had {0} initialising errors, exiting... ".format(init_status[1]))
    sys.exit()
else:
    print("(+) Pygame initialised successfully ")

# Play Surface
size = width, height = 640, 320
playSurface = pygame.display.set_mode(size)
pygame.display.set_caption("Snake Game")

# FPS controller
fpsController = pygame.time.Clock()

# Game settings
CELLSIZE = 10

assert width % CELLSIZE == 0, "Window width must be a multiple of cell size."
assert height % CELLSIZE == 0, "Window height must be a multiple of cell size."
CELLWIDTH = int(width / CELLSIZE)
CELLHEIGHT = int(height / CELLSIZE)

snakePos = [int(CELLWIDTH/2), int(CELLHEIGHT/2)]
snakeBody = [snakePos[0]]
foodPos = [4, 5]
foodSpawn = False
direction = RIGHT
changeto = ''
score = 0



# Game Over
def gameOver():
    myFont = pygame.font.SysFont('monaco', 72)
    GOsurf = myFont.render("Game Over", True, red)
    GOrect = GOsurf.get_rect()
    GOrect.midtop = (320, 25)
    playSurface.blit(GOsurf, GOrect)
    SFont = pygame.font.SysFont('monaco',10)
    Ssurf = SFont.render("{0}".format(score), True, red)
    Srect = Ssurf.get_rect()
    Srect.midtop = (320, 40)
    playSurface.blit(Ssurf, Srect)
    pygame.display.flip()

    time.sleep(4)
    pygame.quit()
    sys.exit()


#draw game terrain :
def drawGame():
    playSurface.fill(black)
    for pos in snakeBody:
        pygame.draw.rect(playSurface, green, pygame.Rect(pos[0]*CELLSIZE, pos[1]*CELLSIZE, CELLSIZE-1, CELLSIZE-1))
    pygame.draw.rect(playSurface, red, pygame.Rect(foodPos[0]*CELLSIZE, foodPos[1]*CELLSIZE, CELLSIZE, CELLSIZE))
    for i in range(CELLWIDTH):
        pygame.draw.line(playSurface, brown,(i*CELLSIZE,0),(i*CELLSIZE,height))
    for i in range(CELLHEIGHT):
        pygame.draw.line(playSurface, brown,(0,i*CELLSIZE),(width,i*CELLSIZE))

    SFont = pygame.font.SysFont('monaco',30)
    Ssurf = SFont.render("{0}".format(score), True, white)
    Srect = Ssurf.get_rect()
    Srect.midtop = (80, 10)
    playSurface.blit(Ssurf, Srect)
        

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                changeto = RIGHT
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                changeto = LEFT
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                changeto = UP
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                changeto = DOWN
            if event.key == pygame.K_ESCAPE:
                pygame.event.post(pygame.event.Event(pygame.QUIT))

    # Validate direction
    if changeto == LEFT and direction != RIGHT:
        direction = changeto
    if changeto == RIGHT and direction != LEFT:
        direction = changeto
    if changeto == UP and direction != DOWN:
        direction = changeto
    if changeto == DOWN and direction != UP:
        direction = changeto

    # Update snake position
    if direction == RIGHT:
        snakePos[0] += 1
    if direction == LEFT:
        snakePos[0] -= 1
    if direction == DOWN:
        snakePos[1] += 1
    if direction == UP:
        snakePos[1] -= 1

    # Snake body mechanism
    snakeBody.insert(0, list(snakePos))
    if snakePos == foodPos:
        foodSpawn = False
        score += 1
    else:
        snakeBody.pop()
    if foodSpawn == False:
        foodPos = [random.randrange(1, CELLWIDTH) , random.randrange(1, CELLHEIGHT)]
        foodSpawn = True
   
    drawGame()

    # Self hit
    for block in snakeBody[1:]:
        if snakePos == block:
            gameOver()
    
    pygame.display.flip()
    fpsController.tick(20)
    