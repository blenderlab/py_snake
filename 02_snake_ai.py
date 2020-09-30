'''
SNAKE GAME AI version 0.1
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
red = pygame.Color(255, 255, 255)
green = pygame.Color(255, 255, 255)
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
brown = pygame.Color(165, 42, 42)


# Pygame Init
init_status = pygame.init()

if init_status[1] > 0:
    print("(!) Had {0} initialising errors, exiting... ".format(init_status[1]))
    sys.exit()
else:
    print("(+) Pygame initialised successfully ")

# Play Surface
size = width, height = 640, 320
CELLSIZE = 10
assert width % CELLSIZE == 0, "Window width must be a multiple of cell size."
assert height % CELLSIZE == 0, "Window height must be a multiple of cell size."
CELLWIDTH = int(width / CELLSIZE)
CELLHEIGHT = int(height / CELLSIZE)

playSurface = pygame.display.set_mode(size)

pygame.display.set_caption("Snake Game")
# FPS controller
fpsController = pygame.time.Clock()

# Game settings
delta = 10
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
    pygame.display.flip()
    time.sleep(4)
    pygame.quit()
    sys.exit()


# Show Score
def showScore(choice=1):
    SFont = pygame.font.SysFont('monaco',32)
    Ssurf = SFont.render("Score  :  {0}".format(score), True, black)
    Srect = Ssurf.get_rect()
    if choice == 1:
        Srect.midtop = (80, 10)
    else:
        Srect.midtop = (320, 100)
    playSurface.blit(Ssurf, Srect)

def get_direction_kbd():
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
    if changeto == 'LEFT' and direction != 'LEFT':
        direction = changeto
    if changeto == 'RIGHT' and direction != 'RIGHT':
        direction = changeto
    if changeto == 'UP' and direction != 'DOWN':
        direction = changeto
    if changeto == 'DOWN' and direction != 'UP':
        direction = changeto
    return direction

def get_direction(head, last_direction):
    x=head[0]
    y=head[1]
    if x == 0:
        if y == 0 :
            if last_direction==LEFT:
                DOWN
            else:
                return LEFT
    if x == CELLWIDTH-1:
        if y == 0 :
            if last_direction==RIGHT:
                DOWN
            else:
                return LEFT

    if x == CELLWIDTH-1:
        if y == CELLHEIGHT-1 :
            if last_direction==LEFT:
                UP
            else:
                return RIGHT
    if x == 0:
        if y == CELLHEIGHT -1:
            if last_direction==LEFT:
                UP
            else:
                return RIGHT
    if x==CELLWIDTH-1:
        if last_direction==RIGHT:
            return random.choice([UP,DOWN])
        else :
            return LEFT
    if y==CELLHEIGHT-1:
        return random.choice([LEFT,RIGHT])
    if x==0:
        if last_direction==LEFT:
            return random.choice([UP,DOWN])
        else :
            return RIGHT
    if y==0:
        return random.choice([LEFT,RIGHT])
    return last_direction

while True:
    
    # get direction with keyboard (manual mode)
    #direction = get_direction_kbd()
    
    # get direction from algorithm (auto mode) : 
    direction = get_direction(snakePos,direction)
    print(direction)
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
        foodPos = [random.randrange(1, CELLWIDTH-1) , random.randrange(1,CELLHEIGHT-1)]
        foodSpawn = True


    playSurface.fill(black)
    for pos in snakeBody:
        pygame.draw.rect(playSurface, green, pygame.Rect(pos[0]*delta, pos[1]*delta, delta, delta))
    pygame.draw.rect(playSurface, brown, pygame.Rect(foodPos[0]*delta, foodPos[1]*delta, delta, delta))
   
    # Getting out of bounds
    if snakePos[0] < 0 or snakePos[0] >= CELLWIDTH:
        gameOver()
    if snakePos[1] < 0 or snakePos[1] >= CELLHEIGHT:
        gameOver()

    # Self hit
    for block in snakeBody[1:]:
        if snakePos == block:
            gameOver()
    showScore()
    pygame.display.flip()
    fpsController.tick(20)