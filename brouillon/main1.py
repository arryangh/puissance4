import sys

import pygame

pygame.init()

# écran
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# grille
CELL_SIZE = 40
espace_gauche = 100


# timer
timer = pygame.time.Clock()

# grille
def draw_grille():
    for i in range(0, 10):
        for j in range(0, 10):
            rect = pygame.Rect(CELL_SIZE*i+espace_gauche, CELL_SIZE*j, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, "red", rect, width=1)


i = 0
while True:
    i += 1
    print(f"{i} ", end="")
    if (i%20 == 0):
        print("")
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill(pygame.Color("white"))
    draw_grille()
    timer.tick(60)
    pygame.display.update()