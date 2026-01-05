import random
import sys
import time

import pygame

pygame.init()

# écran
SCREEN_WIDTH = 1450
SCREEN_HEIGHT = 830
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# timer
timer = pygame.time.Clock()


#object:
class Rect():
    def __init__(self, color, points_list = [(200, 0), (300, 360)]):
        self.color = color
        self.x_direction = "right"
        self.y_direction = "down"

        self.points_list = points_list
        self.rect = pygame.Rect(self.points_list[0][0], self.points_list[0][1], 50, 50)


    # gérer tout
    def manage(self):
        self.draw()
        self.set_direction()
        self.movement()

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect, width=1)

    def set_direction(self):
        y2 = SCREEN_HEIGHT - 50
        y1 = 0
        x2 = SCREEN_WIDTH - 50
        x1 = 0

        if self.rect.y >= y2:
            self.y_direction = "up"

        if self.rect.y <= y1:
            self.y_direction = "down"

        if self.rect.x >= x2:
            self.x_direction = "left"

        if self.rect.x <= x1:
            self.x_direction = "right"

    def movement(self):
        delta_x = 4
        delta_y = 2

        y2 = self.points_list[1][1]
        y1 = self.points_list[0][1]
        x2 = self.points_list[1][0]
        x1 = self.points_list[0][0]


        if self.y_direction == "down":
            self.rect.y += delta_y
            if self.rect.y > y2:
                self.rect.y = y2

        if self.y_direction == "up":
            self.rect.y -= delta_y
            if self.rect.y < y1:
                self.rect.y = y1

        if self.x_direction == "left":
            self.rect.x -= delta_x
            if self.rect.x < x1:
                self.rect.x = x1

        if self.x_direction == "right":
            self.rect.x += delta_x
            if self.rect.x > x2:
                self.rect.x = x2







colors = ["red", "blue", "green", "yellow", "brown", "white", "purple", "orange", "pink", "cyan"]
rect_list = []
for i in range(0, 10000):
    # time.sleep(0.01)
    # x1 = random.randint(0, 40)
    # x2 = random.randint(450, 650)
    # y1 = random.randint(0, 40)
    # y2 = random.randint(300, 400)



    x1 = random.randint(0, SCREEN_WIDTH - 50)
    x2 = random.randint(0, SCREEN_WIDTH - 50)
    y1 = random.randint(0, SCREEN_HEIGHT - 50)
    y2 = random.randint(0, SCREEN_HEIGHT - 50)

    rect = Rect(colors[(10-i)%10], [(x1, y1), (x2, y2)])
    rect_list.append(rect)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()


    screen.fill(pygame.Color("black"))

    for rect in rect_list:
        rect.manage()

    timer.tick(600)
    pygame.display.update()