import random

import pygame
from pygame.locals import *

from horton.grid import Torus
from horton.render.pg import render_grid


SCREEN_W, SCREEN_H = (640, 480)
GRID_W, GRID_H = (300, 300)
GRID_PADDING = 4
FONT_COLOUR = (0, 0, 255)


pygame.init()
pygame.font.init()

screen = pygame.display.set_mode((640, 480))
font = pygame.font.Font(None, 18)


running = 1
world = Torus.from_array(5, 5,
                         [0, 0, 1, 0, 0,
                          1, 1, 0, 1, 1,
                          0, 0, 1, 0, 0,
                          1, 0, 0, 0, 1,
                          1, 1, 1, 1, 1])


while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = 0
        elif event.type == KEYDOWN:
            if event.key == K_EQUALS:
                GRID_PADDING += 1
            elif event.key == K_MINUS:
                if GRID_PADDING >= 1:
                    GRID_PADDING -= 1
            elif event.key == K_RIGHT:
                GRID_W += 1
            elif event.key == K_LEFT:
                if GRID_W > 1:
                    GRID_W -= 1
            elif event.key == K_UP:
                GRID_H += 1
            elif event.key == K_DOWN:
                if GRID_H > 1:
                    GRID_H -= 1

    random_cell = random.choice(world.items())
    if random_cell[1]:
        world[random_cell[0]] = 0
    else:
        world[random_cell[0]] = 1

    screen.fill((255, 255, 255))
    render_grid(screen, world,
                (SCREEN_W / 2) - (GRID_W / 2),
                (SCREEN_H / 2) - (GRID_H / 2),
                GRID_W, GRID_H,
                padding=GRID_PADDING)
    grid_w = font.render("GRID_W: %s" % GRID_W, True, FONT_COLOUR)
    grid_h = font.render("GRID_H: %s" % GRID_H, True, FONT_COLOUR)
    grid_pad = font.render("GRID_PADDING: %s" % GRID_PADDING, True, FONT_COLOUR)
    screen.blit(grid_w, (0, SCREEN_H - 40))
    screen.blit(grid_h, (0, SCREEN_H - 25))
    screen.blit(grid_pad, (0, SCREEN_H - 10))
    pygame.display.flip()


pygame.quit()
