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
from random import randint

#directions
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4
NONE=0
# Colors
red = pygame.Color(255, 20, 20)
green = pygame.Color(20, 255,20)
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
brown = pygame.Color(20, 22, 22)

class SnakeGame:
    def __init__(self, board_width = 20, board_height = 20, gui = False):
        self.score = 0
        self.done = False
        self.board = {'width': board_width, 'height': board_height}
        self.gui = gui
        if gui : self.renderInit()

    def start(self):
        self.snake_init()
        self.generate_food()
        return self.generate_observations()

    def snake_init(self):
        x = randint(5, self.board["width"] - 5)
        y = randint(5, self.board["height"] - 5)
        self.snake = []
        for i in range(3):
            point = [x+i , y]
            self.snake.insert(0, point)

    def generate_food(self):
        food = []
        while food == []:
            food = [randint(1, self.board["width"]), randint(1, self.board["height"])]
            if food in self.snake: food = []
        self.food = food

    def renderInit(self):
           # Pygame Init
        init_status = pygame.init()

        if init_status[1] > 0:
            print("(!) Had {0} initialising errors, exiting... ".format(init_status[1]))
            sys.exit()
        else:
            print("(+) Pygame initialised successfully ")

        # Play Surface
        self.size = (self.board['width']+1)*10, (self.board['width']+1)*10
        self.playSurface = pygame.display.set_mode(self.size)
        pygame.display.set_caption("Snake Game")

        # FPS controller
        self.fpsController = pygame.time.Clock()

        # Game settings
        self.CELLSIZE = 10

      
        
    def render(self):
        self.playSurface.fill(black)
    
        for pos in self.snake:
            pygame.draw.rect(self.playSurface, green, pygame.Rect(pos[0]*self.CELLSIZE, pos[1]*self.CELLSIZE, self.CELLSIZE-1, self.CELLSIZE-1))
        
        pygame.draw.rect(self.playSurface, red, pygame.Rect(self.food[0]*self.CELLSIZE, self.food[1]*self.CELLSIZE, self.CELLSIZE, self.CELLSIZE))
    
        for i in range(self.board['width']+1):
            pygame.draw.line(self.playSurface, brown,(i*self.CELLSIZE,0),(i*self.CELLSIZE,self.board['height']*10))
        for i in range(self.board['width']+1):
            pygame.draw.line(self.playSurface, brown,(0,i*self.CELLSIZE),(self.board['width']*10,i*self.CELLSIZE))

        SFont = pygame.font.SysFont('monaco',30)
        Ssurf = SFont.render("{0}".format(0), True, white)
        Srect = Ssurf.get_rect()
        Srect.midtop = (80, 10)
        self.playSurface.blit(Ssurf, Srect)
        pygame.display.flip()
        self.fpsController.tick(20)
       

    def step(self, key):
        # 0 - UP
        # 1 - RIGHT
        # 2 - DOWN
        # 3 - LEFT
        if self.done == True: self.end_game()
        self.create_new_point(key)
        if self.food_eaten():
            self.score += 1
            self.generate_food()
        else:
            self.remove_last_point()
        self.check_collisions()
        if self.gui : self.render()
        return self.generate_observations()

    def create_new_point(self, key):
        new_point = [self.snake[0][0], self.snake[0][1]]
        if key == 0:
            new_point[0] -= 1
        elif key == 1:
            new_point[1] += 1
        elif key == 2:
            new_point[0] += 1
        elif key == 3:
            new_point[1] -= 1
        self.snake.insert(0, new_point)

    def remove_last_point(self):
        self.snake.pop()

    def food_eaten(self):
        return self.snake[0] == self.food

    def check_collisions(self):
        if (self.snake[0][0] == 0 or
            self.snake[0][0] == self.board["width"] + 1 or
            self.snake[0][1] == 0 or
            self.snake[0][1] == self.board["height"] + 1 or
            self.snake[0] in self.snake[1:-1]):
            self.done = True

    def generate_observations(self):
        return self.done, self.score, self.snake, self.food

    def render_destroy(self):
        pass

    def end_game(self):
        if self.gui: self.render_destroy()
        raise Exception("Game over")

if __name__ == "__main__":
    
  
    game = SnakeGame(gui = True)
    game.start()
    for _ in range(200):
        game.step(randint(0,3))
