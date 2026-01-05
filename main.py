import random
import sys
import time
import pygame

class Block:
    def __init__(self, x_pos, y_pos):
        self.x = x_pos
        self.y = y_pos




pygame.init()

NB_COL = 12
NB_ROW = 12
CELL_SIZE = 50

# screen = pygame.display.set_mode((NB_COL * CELL_SIZE, NB_ROW * CELL_SIZE))
screen = pygame.display.set_mode((1200, 630))


game_on = True
timer = pygame.time.Clock()




def show_grid():
    for i in range(0, NB_COL):
        for j in range(0, NB_ROW):
            rect = pygame.Rect(300+i * CELL_SIZE, 22+j * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, pygame.Color("red"), rect, width=1)


while game_on:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()



    screen.fill(pygame.Color("white"))
    show_grid()
    pygame.display.update()
    timer.tick(60)