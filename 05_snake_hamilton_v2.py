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
green = pygame.Color(20, 255,20)
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
snakePos = [int(CELLWIDTH/2), int(CELLHEIGHT/2)]
snakeBody = [snakePos[0]]
foodPos = [4, 5]
foodSpawn = False
direction = RIGHT
changeto = ''
score = 0


# Game Over
def gameOver():
    myFont = pygame.font.SysFont('Retro Computer', 42)
    GOsurf = myFont.render("Game Over", True, red)
    GOrect = GOsurf.get_rect()
    GOrect.midtop = (320, 25)
    playSurface.blit(GOsurf, GOrect)
    showScore(0)
    pygame.display.flip()
    time.sleep(4)
    pygame.quit()
    sys.exit()


# Show Score
def showScore(choice=1):
    SFont = pygame.font.SysFont('Retro Computer',22)
    Ssurf = SFont.render("Score  :  {0}".format(score), True, white)
    Srect = Ssurf.get_rect()
    if choice == 1:
        Srect.midtop = (80, 10)
    else:
        Srect.midtop = (320, 100)
    playSurface.blit(Ssurf, Srect)

def draw_game():
    id = 255
    playSurface.fill(black)

    for pos in snakeBody:
        id=id-5
        id = max(id,20)
        c= pygame.Color(20, id,20)
        pygame.draw.rect(playSurface, c, pygame.Rect(pos[0]*CELLSIZE, pos[1]*CELLSIZE, CELLSIZE-1, CELLSIZE-1))
    pygame.draw.rect(playSurface, brown, pygame.Rect(foodPos[0]*CELLSIZE, foodPos[1]*CELLSIZE, CELLSIZE-1, CELLSIZE-1))
   
   

def get_direction(head, last_direction,foodPos):
    x=head[0]
    y=head[1]
    if x>foodPos[0]:
        if last_direction==RIGHT:
            return random.choice([UP,DOWN])
        else:
            return LEFT
    if x<foodPos[0]:
        if last_direction==LEFT:
            return random.choice([UP,DOWN])
        else:
            return RIGHT
    if x==foodPos[0]:
        if y>foodPos[1]:
            if last_direction==DOWN:
                return random.choice([LEFT,RIGHT])
            else:
                return UP
        if y<foodPos[1]:
            if last_direction==UP:
                return random.choice([LEFT,RIGHT])
            else:
                return DOWN
         
    return last_direction

while True:
    
    # get direction with keyboard (manual mode)
    #direction = get_direction_kbd()
    
    # get direction from algorithm (auto mode) : 
    direction = get_direction(snakePos,direction,foodPos)
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
        foodPos = [random.randrange(1, CELLWIDTH) , random.randrange(1,CELLHEIGHT)]
        foodSpawn = True


    draw_game()
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
    fpsController.tick(60)