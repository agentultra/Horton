#!/usr/bin/env python
"""
labyrinth.py -- beware ye who enter!

A short game of exploration and perma-death. And reincarnation. And
death.

(c) 2013 James King
"""

import functools
import pygame

from horton.render.pg import render_grid
from pygame.locals import *

import levels


SCREEN_W, SCREEN_H = (640, 480)
SCREEN_BLANK_COLOUR = (0, 0, 0)

DEPTH = 1


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
        if event.type == KEYDOWN:
            move = functools.partial(levels.move_player, level)
            if event.key == K_ESCAPE:
                running = False
            elif event.key == K_w:
                move("north")
            elif event.key == K_s:
                move("south")
            elif event.key == K_d:
                move("east")
            elif event.key == K_a:
                move("west")
            levels.render_level(screen, level)

    pygame.display.flip()
