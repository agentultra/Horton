import random

import pygame
from pygame.locals import *

from horton.grid import Torus
from horton.render.pg import render_grid


pygame.init()
screen = pygame.display.set_mode((640, 480))


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

    random_cell = random.choice(world.items())
    if random_cell[1]:
        world[random_cell[0]] = 0
    else:
        world[random_cell[0]] = 1

    screen.fill((255, 255, 255))
    render_grid(screen, world, 10, 10, 400, 400, padding=2)
    pygame.display.flip()


pygame.quit()
