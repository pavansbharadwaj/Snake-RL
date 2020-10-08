#Snake Tutorial Python

import math
import random
import pygame
import tkinter as tk
from tkinter import messagebox

class cube(object):
    rows = 5
    headersize = 50
    w = 400

    def __init__(self,start,dirnx=1,dirny=0,color=(0,200,0)):
        self.pos = start
        self.dirnx = 1
        self.dirny = 0
        self.color = color

    def move(self, dirnx, dirny):
        self.dirnx = dirnx
        self.dirny = dirny
        self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)  # change our position     
    
    def draw(self, surface, eyes=False):
            dis = self.w // self.rows  # Width/Height of each cube
            i = self.pos[0] # Current row
            j = self.pos[1] # Current Column
    
            pygame.draw.rect(surface, self.color, (i*dis+1,j*dis+1 + headersize, dis-2, dis-2))
            # By multiplying the row and column value of our cube by the width and height of each cube we can determine where to draw it
            
            if eyes: # Draws the eyes
                
                centre = dis//2
                radius = 3
                L = 10
                
                if self.dirnx == 1:
                    LeftEye = ((i+1)*dis - L, headersize + (j+1)*dis - L)
                    RightEye = ((i+1)*dis - L, headersize + j*dis + L)
                if self.dirnx == -1: 
                    LeftEye = (i*dis+L , headersize + (j+1)*dis - L)
                    RightEye = (i*dis+L , headersize + j*dis + L)
                if self.dirny == 1: 
                    LeftEye = (i*dis+L, headersize + (j+1)*dis - L)
                    RightEye = ((i+1)*dis - L, headersize + (j+1)*dis - L)
                if self.dirny == -1: 
                    LeftEye = (i*dis+L, headersize + j*dis + L)
                    RightEye = ((i+1)*dis - L, headersize + j*dis + L)
                
                pygame.draw.circle(surface, (0,0,0), LeftEye, radius)
                pygame.draw.circle(surface, (0,0,0), RightEye, radius)   
                

class snake(object):
    body = []
    turns = {}
    
    def __init__(self, color, pos):
        self.color = color
        self.head = cube(pos)  # The head will be the front of the snake
        self.body.append(self.head)  # We will add head (which is a cube object)
        # to our body list

        # These will represent the direction our snake is moving
        self.dirnx = 0 
        self.dirny = 1

    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            keys = pygame.key.get_pressed()

            for key in keys:
                if keys[pygame.K_LEFT] and not self.dirnx == 1:
                    self.dirnx = -1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                elif keys[pygame.K_RIGHT] and not self.dirnx == -1:
                    self.dirnx = 1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                elif keys[pygame.K_UP] and not self.dirny == 1:
                    self.dirnx = 0
                    self.dirny = -1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
                    
                elif keys[pygame.K_DOWN] and not self.dirny == -1:
                    self.dirnx = 0
                    self.dirny = 1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
                    
        for i, c in enumerate(self.body):  # Loop through every cube in our body
            
            p = c.pos[:]  # This stores the cubes position on the grid
            
            if p in self.turns:  # If the cubes current position is one where we turned
                turn = self.turns[p]  # Get the direction we should turn      
                
                if turn[0] == -1 and c.pos[0] <= 0: 
                    c.pos = (c.rows, c.pos[1])
                elif turn[0] == 1 and c.pos[0] >= c.rows-1: 
                    c.pos = (-1,c.pos[1])
                elif turn[1] == 1 and c.pos[1] >= c.rows-1: 
                    c.pos = (c.pos[0], -1)
                elif turn[1] == -1 and c.pos[1] <= 0: 
                    c.pos = (c.pos[0],c.rows)
                
                c.move(turn[0],turn[1])  # If we haven't reached the edge just move in our current direction
                
                # Move our cube in that direction

                if i == len(self.body)-1:  # If this is the last cube in our body remove the turn from the dict
                    self.turns.pop(p)
                    
            else:  # If we are not turning the cube
                # If the cube reaches the edge of the screen we will make it appear on the opposite side
                if c.dirnx == -1 and c.pos[0] <= 0: c.pos = (c.rows-1, c.pos[1])
                elif c.dirnx == 1 and c.pos[0] >= c.rows-1: c.pos = (0,c.pos[1])
                elif c.dirny == 1 and c.pos[1] >= c.rows-1: c.pos = (c.pos[0], 0)
                elif c.dirny == -1 and c.pos[1] <= 0: c.pos = (c.pos[0],c.rows-1)
                else: c.move(c.dirnx,c.dirny)  # If we haven't reached the edge just move in our current direction
 
    def reset(self, pos):
        self.head = cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.dirnx = 0
        self.dirny = 1

    def addCube(self):
        tail = self.body[-1]
        dx, dy = tail.dirnx, tail.dirny
        
        # We need to know which side of the snake to add the cube to.
        # So we check what direction we are currently moving in to determine if we
        # need to add the cube to the left, right, above or below.
        if dx == 1 and dy == 0:
            self.body.append(cube((tail.pos[0]-1,tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(cube((tail.pos[0]+1,tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(cube((tail.pos[0],tail.pos[1]-1)))
        elif dx == 0 and dy == -1:
            self.body.append(cube((tail.pos[0],tail.pos[1]+1)))
        
        # We then set the cubes direction to the direction of the snake.
        self.body[-1].dirnx = dx
        self.body[-1].dirny = dy
        
    def draw(self, surface):
        for i, c in enumerate(self.body):
            if i == 0:  # for the first cube in the list we want to draw eyes
                c.draw(surface, True)  # adding the true as an argument will tell us to draw eyes
            else:
                c.draw(surface)  # otherwise we will just draw a cube


def drawGrid(surface):
    w = width
    sizeBtwn = w // rows  # Gives us the distance between the lines
    checkboard_n = 0
    
    x = 0  # Keeps track of the current x
    y = 0  # Keeps track of the current y
    for y in range(rows):
        for x in range(rows):
            rect = pygame.Rect(x*sizeBtwn, y*sizeBtwn + headersize, sizeBtwn, sizeBtwn)  
            if checkboard_n == 0:    
                pygame.draw.rect(surface, (30,30,30,0.1), rect)
                checkboard_n = 1
            else: 
                pygame.draw.rect(surface, (60,60,60,0.1), rect)
                checkboard_n = 0
    
    
def redrawWindow(surface):
    #global rows, width, s, snack, headersize
    
    surface.fill((0,0,0))  # Fills the screen with black
    drawGrid(surface)  # Will draw our grid lines
    s.draw(surface) # Draw the snake
    snack.draw(surface)
    
    score_string = 'Score: {}'.format(score)
    font = pygame.font.Font(None,40)
    text = font.render(score_string, 1, (255,255,255))
    surface.blit(text, (15,15))    
    
    pygame.display.update()  # Updates the screen


def randomSnack(rows, item):

    positions = item.body  # Get all the posisitons of cubes in our snake

    while True:  # Keep generating random positions until we get a valid one
        x = random.randrange(rows)
        y = random.randrange(rows)
        if len(list(filter(lambda z:z.pos == (x,y), positions))) > 0:
            # This wll check if the position we generated is occupied by the snake
            continue
        else:
            break

    return (x,y)


def message_box(subject, content):
    pass


def main(): 
    global width, rows, s, snack, headersize, score
    headersize = 50
    width = 400  # Width of our screen
    height = 400  # Height of our screen
    rows = 5  # Amount of rows

    win = pygame.display.set_mode((width, height + headersize))  # Creates our screen object

    s = snake((0,255,0), (0,0))  # Creates a snake object which we will code later
    snack = cube(randomSnack(rows, s), color=(255,0,0))
    clock = pygame.time.Clock() # creating a clock object

    # Main loop
    flag = True

    clock = pygame.time.Clock()
    score = 0
    
    while flag:
        pygame.time.delay(50)
        clock.tick(10)
        s.move()
        
        if s.body[0].pos == snack.pos:
            #s.addCube() # Disable if we only want to try the head
            snack = cube(randomSnack(rows, s), color=(255,0,0))
            score += 1
        
        for x in range(len(s.body)):
            if s.body[x].pos in list(map(lambda z:z.pos,s.body[x+1:])):
                print('Score: ', score)
                message_box('You Lost!', 'Play again...')
                s.reset((0,0))
                score = 0
                break
        
            
        redrawWindow(win)

pygame.init()
main()