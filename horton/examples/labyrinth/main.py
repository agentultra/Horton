#!/usr/bin/env python
"""
labyrinth.py -- beware ye who enter!

A short game of exploration and perma-death. And reincarnation. And
death.  By James King.

(c) 2013 James King
"""

import pygame

from horton.render.pg import render_grid
from pygame.locals import *

import levels


SCREEN_W, SCREEN_H = (640, 480)
SCREEN_BLANK_COLOUR = (0, 0, 0)

DEPTH = 1

# Main game loop

pygame.init()
pygame.display.set_caption("Labyrinth!")

screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
screen.fill(SCREEN_BLANK_COLOUR)

# TODO: remove me! just some test code
level = levels.generate_level(1)
levels.render_level(screen, level)
# end TODO

running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    pygame.display.flip()

# End main game loop
